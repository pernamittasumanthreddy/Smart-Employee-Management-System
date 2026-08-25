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
from apps.notifications.services import NotificationService
from apps.permissions.decorators import hr_or_admin_required


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
