import calendar
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.announcements.forms import AnnouncementForm
from apps.announcements.models import (
    Announcement,
    CompanyEvent,
    EventRegistration,
)
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.leave_management.models import LeaveRequest
from apps.notifications.services import NotificationService
from apps.permissions.decorators import hr_or_admin_required
from apps.shifts.models import CompanyHoliday


@login_required
def announcement_board_view(request):
    dept_id = request.GET.get('department')
    today = timezone.now().date()

    announcements = Announcement.objects.filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gte=today)
    ).select_related('target_department', 'created_by')

    if dept_id:
        announcements = announcements.filter(Q(target_department_id=dept_id) | Q(target_department__isnull=True))

    upcoming_events = CompanyEvent.objects.filter(event_date__gte=timezone.now()).order_by('event_date')[:5]

    return render(request, 'announcements/board.html', {
        'announcements': announcements,
        'upcoming_events': upcoming_events,
        'selected_dept': dept_id,
    })


@login_required
@hr_or_admin_required
def announcement_create_view(request):
    form = AnnouncementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        annc = form.save(commit=False)
        current_emp = getattr(request.user, 'employee_profile', None)
        annc.created_by = current_emp
        annc.save()

        # Broadcast notification locally to active users
        active_users = User.objects.filter(is_active=True).exclude(id=request.user.id)
        NotificationService.broadcast_notification(
            users=active_users,
            title="Company Announcement",
            message=f"New bulletin published: '{annc.title}'",
            category='ANNC',
            link="/announcements/"
        )

        messages.success(request, f"Announcement '{annc.title}' published to company board.")
        return redirect('announcements:board')

    return render(request, 'announcements/announcement_form.html', {'form': form, 'title': 'Publish Company Announcement'})


@login_required
def event_list_view(request):
    events = CompanyEvent.objects.all().prefetch_related('registrations__employee').order_by('event_date')
    return render(request, 'announcements/events.html', {'events': events})


@login_required
def event_register_action(request, event_id):
    event = get_object_or_404(CompanyEvent, id=event_id)
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('announcements:events')

    _reg, created = EventRegistration.objects.get_or_create(event=event, employee=employee)
    if created:
        messages.success(request, f"You are registered for '{event.title}'.")
    else:
        messages.info(request, f"You are already registered for '{event.title}'.")
    return redirect('announcements:events')


@login_required
def workspace_calendar_view(request):
    """
    Interactive Corporate Workplace Calendar & Celebrations Hub:
    Unifies Birthdays, Work Anniversaries, Company Holidays, Approved Leaves, and Townhalls/Events.
    """
    today = timezone.now().date()
    category_filter = request.GET.get('category', 'all')
    month_filter = int(request.GET.get('month', today.month))
    year_filter = int(request.GET.get('year', today.year))

    # Calculate month bounds
    num_days = calendar.monthrange(year_filter, month_filter)[1]
    start_of_month = date(year_filter, month_filter, 1)
    end_of_month = date(year_filter, month_filter, num_days)

    calendar_items = []

    # 1. Company Holidays
    if category_filter in ['all', 'holidays']:
        holidays = CompanyHoliday.objects.filter(
            date__gte=start_of_month,
            date__lte=end_of_month
        )
        for h in holidays:
            calendar_items.append({
                'title': h.name,
                'category': 'holiday',
                'category_label': 'Company Holiday',
                'badge_class': 'bg-info-subtle text-info border border-info-subtle',
                'icon': 'bi-award-fill',
                'date': h.date,
                'description': h.description or 'Public / Company Declared Holiday',
                'action_url': None,
                'action_label': None,
            })

    # 2. Company Events & Townhalls
    if category_filter in ['all', 'events']:
        events = CompanyEvent.objects.filter(
            event_date__date__gte=start_of_month,
            event_date__date__lte=end_of_month
        )
        for e in events:
            calendar_items.append({
                'title': e.title,
                'category': 'event',
                'category_label': 'Corporate Event',
                'badge_class': 'bg-purple-subtle text-purple border border-purple-subtle',
                'icon': 'bi-broadcast',
                'date': e.event_date.date(),
                'time': e.event_date.strftime('%H:%M'),
                'description': f"{e.location or 'Online'} • {e.description or ''}",
                'action_url': f"/announcements/events/{e.id}/register/",
                'action_label': 'RSVP / Register',
            })

    # 3. Approved Leaves & Out of Office
    if category_filter in ['all', 'leaves']:
        leaves = LeaveRequest.objects.filter(
            status='APPROVED',
            start_date__lte=end_of_month,
            end_date__gte=start_of_month
        ).select_related('employee', 'employee__department')
        for l in leaves:
            calendar_items.append({
                'title': f"{l.employee.full_name} — On Leave",
                'category': 'leave',
                'category_label': 'Approved Leave',
                'badge_class': 'bg-warning-subtle text-warning border border-warning-subtle',
                'icon': 'bi-person-slash',
                'date': l.start_date,
                'end_date': l.end_date,
                'description': f"{l.employee.department.name if l.employee.department else 'General'} • {l.get_leave_type_display() if hasattr(l, 'get_leave_type_display') else 'Leave'}",
                'action_url': None,
                'action_label': None,
            })

    # 4. Employee Birthdays & Work Anniversaries
    if category_filter in ['all', 'birthdays']:
        active_employees = Employee.objects.filter(employment_status='ACTIVE').select_related('department')
        for emp in active_employees:
            # Birthday
            if emp.date_of_birth and emp.date_of_birth.month == month_filter:
                b_day = min(emp.date_of_birth.day, num_days)
                b_date = date(year_filter, month_filter, b_day)
                calendar_items.append({
                    'title': f"🎂 Birthday: {emp.full_name}",
                    'category': 'birthday',
                    'category_label': 'Birthday Celebration',
                    'badge_class': 'bg-danger-subtle text-danger border border-danger-subtle',
                    'icon': 'bi-gift-fill',
                    'date': b_date,
                    'description': f"{emp.department.name if emp.department else 'Team'} • Wish them a fantastic birthday!",
                    'action_url': '/recognition/',
                    'action_label': 'Send Kudos',
                })

            # Work Anniversary
            if emp.date_of_joining and emp.date_of_joining.month == month_filter:
                years_completed = year_filter - emp.date_of_joining.year
                if years_completed > 0:
                    a_day = min(emp.date_of_joining.day, num_days)
                    a_date = date(year_filter, month_filter, a_day)
                    calendar_items.append({
                        'title': f"🎉 {years_completed}-Year Work Anniversary: {emp.full_name}",
                        'category': 'anniversary',
                        'category_label': 'Work Anniversary',
                        'badge_class': 'bg-success-subtle text-success border border-success-subtle',
                        'icon': 'bi-trophy-fill',
                        'date': a_date,
                        'description': f"Joined in {emp.date_of_joining.year} • Celebrating {years_completed} year(s) of impact!",
                        'action_url': '/recognition/',
                        'action_label': 'Congratulate',
                    })

    # Sort items chronologically
    calendar_items.sort(key=lambda x: x['date'])

    month_name = calendar.month_name[month_filter]
    month_choices = [(i, calendar.month_name[i]) for i in range(1, 13)]
    year_choices = [today.year - 1, today.year, today.year + 1]

    # Stats
    stats = {
        'total_items': len(calendar_items),
        'holidays': sum(1 for x in calendar_items if x['category'] == 'holiday'),
        'events': sum(1 for x in calendar_items if x['category'] == 'event'),
        'leaves': sum(1 for x in calendar_items if x['category'] == 'leave'),
        'celebrations': sum(1 for x in calendar_items if x['category'] in ['birthday', 'anniversary']),
    }

    return render(request, 'announcements/workspace_calendar.html', {
        'calendar_items': calendar_items,
        'month_filter': month_filter,
        'year_filter': year_filter,
        'month_name': month_name,
        'month_choices': month_choices,
        'year_choices': year_choices,
        'category_filter': category_filter,
        'stats': stats,
    })
