import pytest
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.recognition.models import RecognitionCategory, EmployeeRecognition
from datetime import date

@pytest.mark.django_db
def test_kudos():
    u1 = User.objects.create_user(username='u1', email='u1@test.com', password='Password@123')
    u2 = User.objects.create_user(username='u2', email='u2@test.com', password='Password@123')
    e1 = Employee.objects.create(user=u1, employee_id='EMP-K1', first_name='E1', last_name='User', email='u1@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    e2 = Employee.objects.create(user=u2, employee_id='EMP-K2', first_name='E2', last_name='User', email='u2@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cat = RecognitionCategory.objects.create(name='Speed', points=50)
    rec = EmployeeRecognition.objects.create(sender=e1, recipient=e2, category=cat, title='Great Work', message='Thanks for quick help!')
    assert rec.recipient == e2
