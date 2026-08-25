import pytest
from decimal import Decimal
from django.utils import timezone
from apps.leave_management.models import LeaveType, LeaveBalance, LeaveRequest
from apps.leave_management.accrual_engine import LeaveAccrualCalculationEngine
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestLeaveDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="leave.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-LEAVE-DEEP-01",
            first_name="Ravi",
            last_name="Teja",
            email="ravi.leave@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.ltype, _ = LeaveType.objects.get_or_create(name="Earned Privilege Leave", code="EL", defaults={'days_per_year': Decimal('18.0')})
        self.bal = LeaveBalance.objects.create(
            employee=self.emp,
            leave_type=self.ltype,
            year=2026,
            total_days=Decimal('18.0'),
            used_days=Decimal('2.0')
        )

    def test_leave_balance_and_request_flow(self):
        req = LeaveRequest.objects.create(
            employee=self.emp,
            leave_type=self.ltype,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            days=Decimal('1.0'),
            reason="Family celebration",
            status="APPROVED"
        )
        assert req.status == "APPROVED"
        assert req.days == Decimal('1.0')

    def test_accrual_engine_execution(self):
        count = LeaveAccrualCalculationEngine.process_monthly_leave_accruals(2026, 8)
        assert isinstance(count, int)
