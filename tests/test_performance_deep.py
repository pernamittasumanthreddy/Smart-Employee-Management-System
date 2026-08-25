import pytest
from decimal import Decimal
from django.utils import timezone
from apps.performance.models import PerformanceEvaluation, ReviewCycle
from apps.performance.okr_tracking_engine import OKRProgressTrackingEngine
from apps.goals.models import Goal
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestPerformanceDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="perf.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-PERF-DEEP-01",
            first_name="Neha",
            last_name="Kakkar",
            email="neha.perf@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.cycle, _ = ReviewCycle.objects.get_or_create(
            title="Q3 2026 Appraisal",
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            status="ACTIVE"
        )

    def test_performance_evaluation_submission(self):
        eval_record = PerformanceEvaluation.objects.create(
            employee=self.emp,
            cycle=self.cycle,
            evaluator=self.emp,
            self_rating=5,
            manager_rating=4,
            overall_score=Decimal('4.5'),
            review_period="Q3 2026",
            period_start=timezone.now().date(),
            period_end=timezone.now().date(),
            status="COMPLETED"
        )
        assert eval_record.overall_score == Decimal('4.5')

    def test_okr_progress_tracking(self):
        Goal.objects.create(
            employee=self.emp,
            title="Deliver Cloud Native Microservices Architecture",
            target_date=timezone.now().date(),
            progress_percentage=85,
            status="IN_PROGRESS"
        )
        res = OKRProgressTrackingEngine.calculate_employee_okr_progress(self.emp)
        assert res['total_okrs'] == 1
        assert res['average_completion'] == 85.0
        assert res['health_status'] == 'ON_TRACK'
