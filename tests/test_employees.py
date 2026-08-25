import pytest
from datetime import date
from apps.authentication.models import User
from apps.employees.models import Employee, EmploymentStatus, Gender
from apps.employees.services import Employee360Service
from apps.organization.models import Department

@pytest.mark.django_db
def test_employee_and_360_service():
    user = User.objects.create_user(username='emp360', email='360@test.com', password='Password@123')
    dept = Department.objects.create(name='Engineering', code='ENG')
    emp = Employee.objects.create(
        user=user,
        employee_id='EMP-TEST-01',
        first_name='John',
        last_name='Doe',
        email='360@test.com',
        phone='1234567890',
        date_of_birth=date(1990, 1, 1),
        gender=Gender.MALE,
        date_of_joining=date(2025, 1, 1),
        department=dept,
        employment_status=EmploymentStatus.ACTIVE
    )
    assert emp.full_name == 'John Doe'
    profile_360 = Employee360Service.get_full_360_profile(emp)
    assert profile_360['employee'] == emp
