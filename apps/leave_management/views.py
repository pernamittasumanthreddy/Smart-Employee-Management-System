from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.leave_management.forms import LeaveRequestForm
from apps.leave_management.models import (
    LeaveBalance,
    LeaveRequest,
    LeaveStatus,
)
from apps.leave_management.services import LeaveService
from apps.permissions.decorators import manager_or_above_required
from apps.permissions.models import SystemRole


@login_required
def my_leaves_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    current_year = timezone.now().year
    balances = LeaveBalance.objects.filter(employee=employee, year=current_year).select_related('leave_type')
    requests = LeaveRequest.objects.filter(employee=employee).select_related('leave_type', 'reviewed_by').order_by('-created_at')

    return render(request, 'leave_management/my_leaves.html', {
        'balances': balances,
        'requests': requests,
        'current_year': current_year,
    })

@login_required
def apply_leave_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Only registered employees can apply for leaves.")
        return redirect('authentication:dashboard')

    form = LeaveRequestForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        leave_type = form.cleaned_data['leave_type']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        reason = form.cleaned_data['reason']
        attachment = form.cleaned_data.get('attachment')

        _req, success, msg = LeaveService.apply_leave(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            attachment=attachment
        )
        if success:
            messages.success(request, msg)
            return redirect('leave_management:my_leaves')
        else:
            messages.error(request, msg)

    return render(request, 'leave_management/apply_leave.html', {'form': form})

@login_required
@manager_or_above_required
def leave_approval_list_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    is_admin_or_hr = request.user.is_superuser or request.user.role in [SystemRole.ADMIN, SystemRole.HR]

    if is_admin_or_hr:
        pending_requests = LeaveRequest.objects.filter(status=LeaveStatus.PENDING).select_related('employee__department', 'leave_type')
        past_requests = LeaveRequest.objects.exclude(status=LeaveStatus.PENDING).select_related('employee__department', 'leave_type')[:50]
    else:
        # Team manager sees their direct reports or department team members
        if employee:
            q_filter = (Q(employee__reporting_manager=employee) | Q(employee__department=employee.department)) & ~Q(employee=employee)
        else:
            q_filter = Q()
        pending_requests = LeaveRequest.objects.filter(status=LeaveStatus.PENDING).filter(q_filter).select_related('employee__department', 'leave_type')
        past_requests = LeaveRequest.objects.exclude(status=LeaveStatus.PENDING).filter(q_filter).select_related('employee__department', 'leave_type')[:50]

    return render(request, 'leave_management/approval_list.html', {
        'pending_requests': pending_requests,
        'past_requests': past_requests,
    })

@login_required
@manager_or_above_required
def approve_leave_action(request, request_id):
    leave_req = get_object_or_404(LeaveRequest, id=request_id)
    reviewer = getattr(request.user, 'employee_profile', None)
    success, msg = LeaveService.approve_leave(leave_req, reviewer)
    if success:
        messages.success(request, msg)
    else:
        messages.error(request, msg)
    return redirect('leave_management:approval_list')

@login_required
@manager_or_above_required
def reject_leave_action(request, request_id):
    leave_req = get_object_or_404(LeaveRequest, id=request_id)
    reviewer = getattr(request.user, 'employee_profile', None)
    reason = request.POST.get('rejection_reason', 'Declined by manager')
    success, msg = LeaveService.reject_leave(leave_req, reviewer, reason)
    if success:
        messages.warning(request, msg)
    else:
        messages.error(request, msg)
    return redirect('leave_management:approval_list')

@login_required
def leave_calendar_view(request):
    approved_leaves = LeaveRequest.objects.filter(status=LeaveStatus.APPROVED).select_related('employee', 'leave_type')
    return render(request, 'leave_management/calendar.html', {'approved_leaves': approved_leaves})
