import secrets

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.expenses.forms import ExpenseClaimForm
from apps.expenses.models import ExpenseClaim, ExpenseStatus
from apps.notifications.services import NotificationService
from apps.permissions.decorators import hr_or_admin_required, manager_or_above_required


@login_required
def my_expenses_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    claims = ExpenseClaim.objects.filter(employee=employee).select_related('category', 'reviewed_by')
    total_claimed = claims.aggregate(s=Sum('amount'))['s'] or 0
    total_reimbursed = claims.filter(status=ExpenseStatus.REIMBURSED).aggregate(s=Sum('amount'))['s'] or 0

    return render(request, 'expenses/my_expenses.html', {
        'claims': claims,
        'total_claimed': total_claimed,
        'total_reimbursed': total_reimbursed,
    })

@login_required
def claim_expense_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    form = ExpenseClaimForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        claim = form.save(commit=False)
        claim.employee = employee
        claim.claim_number = f"EXP-{timezone.now().year}-{secrets.token_hex(3).upper()}"
        claim.save()

        # Notify reporting manager if present
        if employee.reporting_manager and employee.reporting_manager.user:
            NotificationService.create_notification(
                user=employee.reporting_manager.user,
                title="New Expense Claim",
                message=f"{employee.full_name} submitted an expense claim of ${claim.amount} for '{claim.title}'.",
                category='EXP',
                link="/expenses/approvals/"
            )

        messages.success(request, f"Expense claim [{claim.claim_number}] submitted for approval.")
        return redirect('expenses:my_expenses')

    return render(request, 'expenses/claim_form.html', {'form': form})

@login_required
@manager_or_above_required
def expense_approvals_view(request):
    pending_claims = ExpenseClaim.objects.filter(status=ExpenseStatus.PENDING).select_related('employee__department', 'category')
    processed_claims = ExpenseClaim.objects.exclude(status=ExpenseStatus.PENDING).select_related('employee__department', 'category')[:50]

    return render(request, 'expenses/approvals.html', {
        'pending_claims': pending_claims,
        'processed_claims': processed_claims,
    })

@login_required
@manager_or_above_required
def approve_expense_action(request, claim_id):
    claim = get_object_or_404(ExpenseClaim, id=claim_id)
    reviewer = getattr(request.user, 'employee_profile', None)
    claim.status = ExpenseStatus.APPROVED
    claim.reviewed_by = reviewer
    claim.reviewed_at = timezone.now()
    claim.save()

    if claim.employee.user:
        NotificationService.create_notification(
            user=claim.employee.user,
            title="Expense Approved",
            message=f"Your expense claim [{claim.claim_number}] for ${claim.amount} has been approved.",
            category='EXP'
        )

    messages.success(request, f"Expense [{claim.claim_number}] approved.")
    return redirect('expenses:approvals')

@login_required
@manager_or_above_required
def reject_expense_action(request, claim_id):
    claim = get_object_or_404(ExpenseClaim, id=claim_id)
    reviewer = getattr(request.user, 'employee_profile', None)
    reason = request.POST.get('rejection_reason', 'Declined')
    claim.status = ExpenseStatus.REJECTED
    claim.reviewed_by = reviewer
    claim.reviewed_at = timezone.now()
    claim.rejection_reason = reason
    claim.save()

    if claim.employee.user:
        NotificationService.create_notification(
            user=claim.employee.user,
            title="Expense Rejected",
            message=f"Your expense claim [{claim.claim_number}] was rejected. Reason: {reason}",
            category='EXP'
        )

    messages.warning(request, f"Expense [{claim.claim_number}] rejected.")
    return redirect('expenses:approvals')

@login_required
@hr_or_admin_required
def reimburse_expense_action(request, claim_id):
    claim = get_object_or_404(ExpenseClaim, id=claim_id)
    claim.status = ExpenseStatus.REIMBURSED
    claim.save()
    messages.success(request, f"Expense [{claim.claim_number}] marked as reimbursed / paid out.")
    return redirect('expenses:approvals')
