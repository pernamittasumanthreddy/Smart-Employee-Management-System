import pytest
from datetime import date, time
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.attendance.services import AttendanceService
from apps.shifts.models import WorkShift, ShiftAssignment

@pytest.mark.django_db
def test_attendance_punch():
    user = User.objects.create_user(username='attuser', email='att@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-ATT-01', first_name='Att', last_name='User', email='att@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    shift = WorkShift.objects.create(name='Day', code='DAY', start_time=time(9, 0), end_time=time(17, 30))
    ShiftAssignment.objects.create(employee=emp, shift=shift, start_date=date(2025, 1, 1))

    rec, success, msg = AttendanceService.check_in(emp)
    assert success is True
    assert rec.check_in_time is not None
    assert rec.status == AttendanceStatus.PRESENT

    rec_out, success_out, msg_out = AttendanceService.check_out(emp)
    assert success_out is True
    assert rec_out.check_out_time is not None
    assert rec_out.total_working_hours >= Decimal('0.00')
