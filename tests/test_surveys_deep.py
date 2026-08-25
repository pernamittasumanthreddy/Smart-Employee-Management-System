import pytest
from django.utils import timezone
from apps.surveys.models import Survey, SurveyQuestion, SurveySubmission, SurveyAnswer
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestSurveysDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="surv.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-SURV-DEEP-01",
            first_name="Varun",
            last_name="Dhawan",
            email="varun.surv@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.surv = Survey.objects.create(
            title="Q3 2026 Employee Net Promoter Score & Culture Pulse",
            survey_type="ENPS",
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            is_active=True
        )
        self.q = SurveyQuestion.objects.create(
            survey=self.surv,
            question_text="On a scale of 0-10, how likely are you to recommend Bharat Enterprise Solutions as a great place to work?",
            question_type="RATING_10",
            order=1
        )

    def test_survey_submission_and_enps(self):
        sub = SurveySubmission.objects.create(
            survey=self.surv,
            employee=self.emp,
            enps_score=10
        )
        ans = SurveyAnswer.objects.create(
            submission=sub,
            question=self.q,
            rating_value=10,
            text_answer="Outstanding leadership, high trust, and world-class engineering standards."
        )
        assert sub.enps_score == 10
        assert ans.rating_value == 10
