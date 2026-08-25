import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.training.models import Course, TrainingEnrollment, EnrollmentStatus

@pytest.mark.django_db
def test_course_enrollment():
    user = User.objects.create_user(username='trainuser', email='train@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-TR-01', first_name='Train', last_name='User', email='train@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    c = Course.objects.create(title='Cybersecurity 101', code='SEC-101', duration_hours=Decimal('8.0'), pass_score=70)
    enr = TrainingEnrollment.objects.create(course=c, employee=emp, status=EnrollmentStatus.COMPLETED, score=Decimal('90.0'))
    assert enr.status == EnrollmentStatus.COMPLETED
