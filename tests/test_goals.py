import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.goals.models import Goal, GoalStatus

@pytest.mark.django_db
def test_goal_progress():
    user = User.objects.create_user(username='gluser', email='gl@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-GL-01', first_name='Goal', last_name='User', email='gl@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    goal = Goal.objects.create(employee=emp, title='Target OKR', target_metric='Revenue', target_value=Decimal('100.0'), current_value=Decimal('80.0'), progress_percentage=80, start_date=date(2026, 1, 1), due_date=date(2026, 12, 31))
    assert goal.progress_percentage == 80
