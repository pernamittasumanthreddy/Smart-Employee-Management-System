import calendar
import csv
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.attendance.services import AttendanceService
from apps.employees.models import Employee
from apps.organization.models import Department
from apps.permissions.decorators import manager_or_above_required
from apps.shifts.models import CompanyHoliday


@login_required
def punch_in_out_action(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Only registered employees can punch attendance.")
        return redirect('authentication:dashboard')

    action = request.POST.get('action')
    ip = request.META.get('REMOTE_ADDR')

    if action == 'check_in':
        record, success, msg = AttendanceService.check_in(employee, ip_address=ip)
        if success:
            messages.success(request, msg)
        else:
            messages.warning(request, msg)
    elif action == 'check_out':
        _record, success, msg = AttendanceService.check_out(employee, ip_address=ip)
        if success:
            messages.success(request, msg)
        else:
            messages.warning(request, msg)
    
    return redirect('attendance:my_attendance')


@login_required
def my_attendance(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile not found.")
        return redirect('authentication:dashboard')

    records = AttendanceRecord.objects.filter(employee=employee).order_by('-date')
    today_record = AttendanceRecord.objects.filter(employee=employee, date=timezone.now().date()).first()

    total_days = records.count()
    present_days = records.filter(status=AttendanceStatus.PRESENT).count()
    late_days = records.filter(is_late=True).count()
    absent_days = records.filter(status=AttendanceStatus.ABSENT).count()
    avg_hours = records.aggregate(avg=Avg('total_working_hours'))['avg'] or 0.0

    return render(request, 'attendance/my_attendance.html', {
        'records': records[:60],
        'today_record': today_record,
        'total_days': total_days,
        'present_days': present_days,
        'late_days': late_days,
        'absent_days': absent_days,
        'avg_hours': round(avg_hours, 1)
    })


@login_required
def monthly_attendance(request):
    """
    Monthly Attendance Overview:
    Detailed calendar breakdown for a specific month and year with statistics,
    daily status pills, working hours, and CSV export.
    """
    user = request.user
    today = timezone.now().date()
    
    # 1. Determine target Year & Month
    try:
        selected_year = int(request.GET.get('year', today.year))
    except (ValueError, TypeError):
        selected_year = today.year

    try:
        selected_month = int(request.GET.get('month', today.month))
        if selected_month < 1 or selected_month > 12:
            selected_month = today.month
    except (ValueError, TypeError):
        selected_month = today.month

    # 2. Determine target Employee
    is_privileged = (
        user.is_superuser or 
        getattr(user, 'role', '') in ['ADMIN', 'HR', 'MANAGER']
    )

    employees_list = None
    if is_privileged:
        employees_list = Employee.objects.filter(employment_status='ACTIVE').select_related('department')

    target_employee_id = request.GET.get('employee_id')
    if is_privileged and target_employee_id:
        target_employee = get_object_or_404(Employee, id=target_employee_id)
    else:
        target_employee = getattr(user, 'employee_profile', None)
        if not target_employee:
            target_employee = Employee.objects.filter(employment_status='ACTIVE').first() or Employee.objects.first()

    if not target_employee:
        messages.error(request, "No employee record found to view attendance.")
        return redirect('authentication:dashboard')

    # 3. Calculate date range for the month
    num_days = calendar.monthrange(selected_year, selected_month)[1]
    start_date = date(selected_year, selected_month, 1)
    end_date = date(selected_year, selected_month, num_days)

    # 4. Fetch records and holidays
    records = AttendanceRecord.objects.filter(
        employee=target_employee,
        date__gte=start_date,
        date__lte=end_date
    )
    records_by_date = {r.date: r for r in records}

    holidays = CompanyHoliday.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    )
    holidays_by_date = {h.date: h.name for h in holidays}

    # 5. Build daily breakdown
    daily_data = []
    stats = {
        'total_days': num_days,
        'working_days': 0,
        'present': 0,
        'half_day': 0,
        'on_leave': 0,
        'holiday': 0,
        'weekly_off': 0,
        'absent': 0,
        'late_count': 0,
        'total_hours': 0.0,
    }

    month_name = calendar.month_name[selected_month]

    for day in range(1, num_days + 1):
        curr_date = date(selected_year, selected_month, day)
        day_of_week = curr_date.strftime('%A')
        is_weekend = curr_date.weekday() in (5, 6) # Saturday or Sunday
        is_holiday = curr_date in holidays_by_date

        record = records_by_date.get(curr_date)

        if is_holiday:
            status_display = 'Holiday'
            badge_class = 'bg-info-subtle text-info border border-info-subtle'
            stats['holiday'] += 1
        elif is_weekend:
            status_display = 'Weekly Off'
            badge_class = 'bg-secondary-subtle text-secondary border border-secondary-subtle'
            stats['weekly_off'] += 1
        else:
            stats['working_days'] += 1
            if record:
                if record.status == AttendanceStatus.PRESENT:
                    status_display = 'Present'
                    badge_class = 'bg-success-subtle text-success border border-success-subtle'
                    stats['present'] += 1
                elif record.status == AttendanceStatus.HALF_DAY:
                    status_display = 'Half Day'
                    badge_class = 'bg-warning-subtle text-warning border border-warning-subtle'
                    stats['half_day'] += 1
                elif record.status == AttendanceStatus.ON_LEAVE:
                    status_display = 'On Leave'
                    badge_class = 'bg-primary-subtle text-primary border border-primary-subtle'
                    stats['on_leave'] += 1
                else:
                    status_display = 'Absent'
                    badge_class = 'bg-danger-subtle text-danger border border-danger-subtle'
                    stats['absent'] += 1
            else:
                if curr_date <= today:
                    status_display = 'Absent'
                    badge_class = 'bg-danger-subtle text-danger border border-danger-subtle'
                    stats['absent'] += 1
                else:
                    status_display = 'Upcoming'
                    badge_class = 'bg-light text-muted border'

        if record:
            if record.is_late:
                stats['late_count'] += 1
            stats['total_hours'] += float(record.total_working_hours or 0.0)

        daily_data.append({
            'date': curr_date,
            'day_num': day,
            'day_name': curr_date.strftime('%a'),
            'full_day_name': day_of_week,
            'is_weekend': is_weekend,
            'is_holiday': is_holiday,
            'holiday_name': holidays_by_date.get(curr_date, ''),
            'record': record,
            'status_display': status_display,
            'badge_class': badge_class,
            'check_in': record.check_in_time if record else None,
            'check_out': record.check_out_time if record else None,
            'hours': record.total_working_hours if record else 0.0,
            'is_late': record.is_late if record else False,
            'late_minutes': record.late_minutes if record else 0,
        })

    # Calculations
    stats['total_hours'] = round(stats['total_hours'], 1)
    stats['avg_daily_hours'] = round(stats['total_hours'] / max(stats['working_days'], 1), 1)
    total_effective_presence = stats['present'] + (stats['half_day'] * 0.5)
    stats['attendance_rate'] = round((total_effective_presence / max(stats['working_days'], 1)) * 100, 1) if stats['working_days'] > 0 else 100.0

    # 6. CSV Export handler
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Monthly_Attendance_{target_employee.employee_id}_{month_name}_{selected_year}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Monthly Attendance Report'])
        writer.writerow(['Employee ID', target_employee.employee_id])
        writer.writerow(['Employee Name', target_employee.full_name])
        writer.writerow(['Department', target_employee.department.name if target_employee.department else 'N/A'])
        writer.writerow(['Month / Year', f"{month_name} {selected_year}"])
        writer.writerow([])
        writer.writerow(['Date', 'Day', 'Status', 'Check In', 'Check Out', 'Total Hours', 'Late (Mins)', 'Notes'])
        
        for item in daily_data:
            writer.writerow([
                item['date'].strftime('%Y-%m-%d'),
                item['day_name'],
                item['status_display'],
                item['check_in'].strftime('%H:%M:%S') if item['check_in'] else '--',
                item['check_out'].strftime('%H:%M:%S') if item['check_out'] else '--',
                item['hours'],
                item['late_minutes'],
                item['holiday_name'] or ''
            ])
            
        writer.writerow([])
        writer.writerow(['SUMMARY STATISTICS'])
        writer.writerow(['Total Working Days', stats['working_days']])
        writer.writerow(['Present Days', stats['present']])
        writer.writerow(['Half Days', stats['half_day']])
        writer.writerow(['On Leave', stats['on_leave']])
        writer.writerow(['Absent Days', stats['absent']])
        writer.writerow(['Total Hours Worked', stats['total_hours']])
        writer.writerow(['Attendance Rate %', f"{stats['attendance_rate']}%"])
        
        return response

    # 7. Generate list of available months and years for dropdowns
    month_choices = [(i, calendar.month_name[i]) for i in range(1, 13)]
    year_choices = [y for y in range(today.year - 2, today.year + 3)]

    return render(request, 'attendance/monthly_attendance.html', {
        'target_employee': target_employee,
        'daily_data': daily_data,
        'stats': stats,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'month_name': month_name,
        'month_choices': month_choices,
        'year_choices': year_choices,
        'employees_list': employees_list,
        'is_privileged': is_privileged,
    })


@login_required
@manager_or_above_required
def attendance_roster(request):
    target_date_str = request.GET.get('date', timezone.now().date().strftime('%Y-%m-%d'))
    dept_id = request.GET.get('department')
    search = request.GET.get('search', '').strip()

    try:
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    except ValueError:
        target_date = timezone.now().date()

    records = AttendanceRecord.objects.filter(date=target_date).select_related('employee__department', 'employee__designation')
    
    if dept_id:
        records = records.filter(employee__department_id=dept_id)
    if search:
        records = records.filter(Q(employee__first_name__icontains=search) | Q(employee__last_name__icontains=search) | Q(employee__employee_id__icontains=search))

    departments = Department.objects.filter(is_active=True)

    # Calculate metrics
    present_count = records.filter(status=AttendanceStatus.PRESENT).count()
    absent_count = records.filter(status=AttendanceStatus.ABSENT).count()
    late_count = records.filter(is_late=True).count()

    return render(request, 'attendance/attendance_roster.html', {
        'records': records,
        'target_date': target_date,
        'departments': departments,
        'selected_dept': dept_id,
        'search': search,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
    })


@login_required
def department_attendance_summary(request):
    departments = Department.objects.filter(is_active=True)
    today = timezone.now().date()
    
    summary_data = []
    for dept in departments:
        emp_count = dept.employees.filter(employment_status='ACTIVE').count()
        present = AttendanceRecord.objects.filter(
            employee__department=dept,
            date=today,
            status=AttendanceStatus.PRESENT
        ).count()
        rate = (present / emp_count * 100) if emp_count > 0 else 0
        
        summary_data.append({
            'department': dept,
            'total_employees': emp_count,
            'present_today': present,
            'attendance_rate': round(rate, 1)
        })
        
    return render(request, 'attendance/department_summary.html', {
        'summary_data': summary_data,
        'today': today
    })


@login_required
def team_radar_view(request):
    """
    Live Workforce Presence Radar:
    Real-time visibility into who is in the office, working remotely, on leave,
    or absent today across all departments.
    """
    today = timezone.now().date()
    dept_id = request.GET.get('department')
    search_q = request.GET.get('search', '').strip()

    employees = Employee.objects.filter(employment_status='ACTIVE').select_related('department', 'designation')

    if dept_id:
        employees = employees.filter(department_id=dept_id)
    if search_q:
        employees = employees.filter(
            Q(first_name__icontains=search_q) |
            Q(last_name__icontains=search_q) |
            Q(employee_id__icontains=search_q)
        )

    # Fetch today's records
    records = AttendanceRecord.objects.filter(date=today)
    records_by_emp = {r.employee_id: r for r in records}

    # Fetch today's approved leaves from leave_management
    from apps.leave_management.models import LeaveRequest
    active_leaves = LeaveRequest.objects.filter(
        status='APPROVED',
        start_date__lte=today,
        end_date__gte=today
    )
    leaves_by_emp = {l.employee_id: l for l in active_leaves}

    team_members = []
    stats = {
        'total': 0,
        'present': 0,
        'half_day': 0,
        'on_leave': 0,
        'absent': 0,
    }

    for emp in employees:
        stats['total'] += 1
        record = records_by_emp.get(emp.id)
        leave = leaves_by_emp.get(emp.id)

        if leave:
            status_text = 'On Leave'
            badge_class = 'bg-primary-subtle text-primary border border-primary-subtle'
            status_indicator = 'bg-primary'
            stats['on_leave'] += 1
        elif record and record.status == AttendanceStatus.PRESENT:
            status_text = 'In Office / Checked-in'
            badge_class = 'bg-success-subtle text-success border border-success-subtle'
            status_indicator = 'bg-success'
            stats['present'] += 1
        elif record and record.status == AttendanceStatus.HALF_DAY:
            status_text = 'Half Day'
            badge_class = 'bg-warning-subtle text-warning border border-warning-subtle'
            status_indicator = 'bg-warning'
            stats['half_day'] += 1
        else:
            status_text = 'Not Checked In'
            badge_class = 'bg-danger-subtle text-danger border border-danger-subtle'
            status_indicator = 'bg-danger'
            stats['absent'] += 1

        team_members.append({
            'employee': emp,
            'status_text': status_text,
            'badge_class': badge_class,
            'status_indicator': status_indicator,
            'record': record,
            'leave': leave,
        })

    departments = Department.objects.filter(is_active=True)

    return render(request, 'attendance/team_radar.html', {
        'team_members': team_members,
        'departments': departments,
        'selected_dept': dept_id,
        'search_q': search_q,
        'stats': stats,
        'today': today,
    })

