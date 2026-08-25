import pytest
from datetime import date, timedelta
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.leave_management.models import LeaveType, LeaveBalance, LeaveRequest
from apps.leave_management.services import LeaveService

@pytest.mark.django_db
def test_leave_service_request_and_approval():
    user = User.objects.create_user(username='leaveuser', email='leave@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-LV-01', first_name='Leave', last_name='User', email='leave@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    lt = LeaveType.objects.create(name='Casual', code='CL', days_per_year=Decimal('12.0'))
    bal = LeaveBalance.objects.create(employee=emp, leave_type=lt, year=2026, total_allocated=Decimal('12.0'))

    req, success, msg = LeaveService.apply_leave(emp, lt, date(2026, 6, 1), date(2026, 6, 3), 'Vacation')
    assert success is True
    assert req.total_days == Decimal('3.0')
    assert req.status == 'PENDING'

    approved, app_success, app_msg = LeaveService.approve_leave(req, reviewer=emp)
    assert app_success is True
    assert approved.status == 'APPROVED'
    bal.refresh_from_db()
    assert bal.used_days == Decimal('3.0')
