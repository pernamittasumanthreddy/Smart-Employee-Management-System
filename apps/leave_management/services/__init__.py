from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.leave_management.models import (
    LeaveBalance,
    LeaveRequest,
    LeaveStatus,
)
from apps.notifications.services import NotificationService


class LeaveService:
    @staticmethod
    def calculate_business_days(start_date, end_date):
        delta = (end_date - start_date).days + 1
        return Decimal(str(delta))

    @staticmethod
    def check_overlapping_requests(employee, start_date, end_date, exclude_id=None):
        query = LeaveRequest.objects.filter(
            employee=employee,
            status__in=[LeaveStatus.PENDING, LeaveStatus.APPROVED],
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        if exclude_id:
            query = query.exclude(id=exclude_id)
        return query.exists()

    @staticmethod
    @transaction.atomic
    def apply_leave(employee, leave_type, start_date, end_date, reason, attachment=None):
        if LeaveService.check_overlapping_requests(employee, start_date, end_date):
            return None, False, "You already have an active or pending leave request for these dates."

        days = LeaveService.calculate_business_days(start_date, end_date)
        current_year = start_date.year

        balance, _ = LeaveBalance.objects.get_or_create(
            employee=employee,
            leave_type=leave_type,
            year=current_year,
            defaults={'total_allocated': leave_type.days_per_year}
        )

        if Decimal(str(balance.remaining_days)) < days:
            return None, False, f"Insufficient leave balance. You have {balance.remaining_days} days available, but requested {days} days."

        # Mark as pending on balance
        balance.pending_days += days
        balance.save()

        leave_req = LeaveRequest.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            total_days=days,
            reason=reason,
            attachment=attachment,
            status=LeaveStatus.PENDING
        )

        # Notify reporting manager if present
        if employee.reporting_manager and employee.reporting_manager.user:
            NotificationService.create_notification(
                user=employee.reporting_manager.user,
                title="New Leave Request",
                message=f"{employee.full_name} submitted a leave request for {days} days ({start_date} to {end_date}).",
                category='LEAVE',
                link="/leave/approvals/"
            )

        return leave_req, True, "Leave request submitted successfully."

    @staticmethod
    @transaction.atomic
    def approve_leave(leave_request, reviewer_employee=None, reviewer=None):
        rev = reviewer_employee or reviewer
        if leave_request.status != LeaveStatus.PENDING:
            return leave_request, False, "Leave request is not in pending status."

        balance = LeaveBalance.objects.filter(
            employee=leave_request.employee,
            leave_type=leave_request.leave_type,
            year=leave_request.start_date.year
        ).first()

        if balance:
            balance.pending_days = max(Decimal('0.0'), balance.pending_days - leave_request.total_days)
            balance.used_days += leave_request.total_days
            balance.save()

        leave_request.status = LeaveStatus.APPROVED
        leave_request.reviewed_by = rev
        leave_request.reviewed_at = timezone.now()
        leave_request.save()

        # In-app notification to employee
        if leave_request.employee.user:
            NotificationService.create_notification(
                user=leave_request.employee.user,
                title="Leave Request Approved",
                message=f"Your {leave_request.leave_type.name} from {leave_request.start_date} to {leave_request.end_date} has been approved.",
                category='LEAVE',
                link="/leave/my-leaves/"
            )

        return leave_request, True, "Leave request approved successfully."

    @staticmethod
    @transaction.atomic
    def reject_leave(leave_request, reviewer_employee, rejection_reason=""):
        if leave_request.status != LeaveStatus.PENDING:
            return False, "Leave request is not in pending status."

        balance = LeaveBalance.objects.filter(
            employee=leave_request.employee,
            leave_type=leave_request.leave_type,
            year=leave_request.start_date.year
        ).first()

        if balance:
            balance.pending_days = max(Decimal('0.0'), balance.pending_days - leave_request.total_days)
            balance.save()

        leave_request.status = LeaveStatus.REJECTED
        leave_request.reviewed_by = reviewer_employee
        leave_request.reviewed_at = timezone.now()
        leave_request.rejection_reason = rejection_reason
        leave_request.save()

        if leave_request.employee.user:
            NotificationService.create_notification(
                user=leave_request.employee.user,
                title="Leave Rejected",
                message=f"Your leave request ({leave_request.start_date} to {leave_request.end_date}) was rejected. Reason: {rejection_reason}",
                category='LEAVE'
            )
        return True, "Leave request rejected."
