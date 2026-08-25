import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.performance.models import ReviewCycle, PerformanceEvaluation

@pytest.mark.django_db
def test_performance_review():
    user = User.objects.create_user(username='perfuser', email='perf@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-PF-01', first_name='Perf', last_name='User', email='perf@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cycle = ReviewCycle.objects.create(title='Q1 Appraisal', code='Q1-2026', start_date=date(2026, 1, 1), end_date=date(2026, 3, 31))
    eval_obj = PerformanceEvaluation.objects.create(
        cycle=cycle,
        employee=emp,
        technical_skills_rating=Decimal('4.5'),
        communication_rating=Decimal('4.0'),
        productivity_rating=Decimal('4.5'),
        leadership_rating=Decimal('4.0'),
        final_score=Decimal('4.25'),
        is_submitted=True
    )
    assert eval_obj.final_score == Decimal('4.25')
