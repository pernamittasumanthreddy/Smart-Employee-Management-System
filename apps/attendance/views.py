from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.attendance.services import AttendanceService
from apps.organization.models import Department
from apps.permissions.decorators import manager_or_above_required


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
@manager_or_above_required
def department_attendance_summary(request):
    today = timezone.now().date()
    departments = Department.objects.filter(is_active=True).annotate(
        total_emp=Count('employees', filter=Q(employees__employment_status='ACTIVE'))
    )
    
    dept_stats = []
    for dept in departments:
        today_records = AttendanceRecord.objects.filter(employee__department=dept, date=today)
        present = today_records.filter(status=AttendanceStatus.PRESENT).count()
        late = today_records.filter(is_late=True).count()
        absent = dept.total_emp - present
        pct = round((present / dept.total_emp * 100), 1) if dept.total_emp > 0 else 0
        dept_stats.append({
            'department': dept,
            'total': dept.total_emp,
            'present': present,
            'late': late,
            'absent': max(0, absent),
            'percentage': pct
        })

    return render(request, 'attendance/department_summary.html', {
        'dept_stats': dept_stats,
        'today': today
    })
