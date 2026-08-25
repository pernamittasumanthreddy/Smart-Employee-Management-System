import pytest
from decimal import Decimal
from django.utils import timezone
from apps.recruitment.models import JobRequisition, Candidate, JobApplication, InterviewSchedule, InterviewFeedback, OfferLetter
from apps.recruitment.matching import CandidateMatchingEngine
from apps.organization.models import Department
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestRecruitmentDeepSuite:
    def setup_method(self):
        self.dept, _ = Department.objects.get_or_create(name="AI & Core Platform", code="ENG-AI")
        self.req = JobRequisition.objects.create(
            title="Lead MLOps Engineer",
            requisition_code="REQ-2026-AI-01",
            department=self.dept,
            headcount=1,
            min_experience_years=Decimal('4.0'),
            max_experience_years=Decimal('8.0'),
            budget_min=Decimal('1800000.00'),
            budget_max=Decimal('2600000.00'),
            required_skills="Python, PyTorch, Kubernetes, Docker, MLflow, AWS",
            target_hire_date=timezone.now().date()
        )
        self.cand = Candidate.objects.create(
            first_name="Ananya",
            last_name="Deshmukh",
            email="ananya.mlops@example.com",
            phone="+91 98200 11223",
            current_company="AI Labs Global",
            current_designation="Senior MLOps Specialist",
            total_experience_years=Decimal('5.5'),
            current_ctc=Decimal('1600000.00'),
            expected_ctc=Decimal('2200000.00'),
            notice_period_days=30,
            current_location="Bengaluru",
            skills_summary="Python, PyTorch, Docker, Kubernetes, MLflow, CI/CD, AWS SageMaker"
        )
        self.app = JobApplication.objects.create(
            job_requisition=self.req,
            candidate=self.cand,
            stage="SCREENING",
            match_score_percentage=92
        )

    def test_candidate_matching_engine_composite(self):
        match_res = CandidateMatchingEngine.calculate_overall_match_index(self.cand, self.req)
        assert match_res['composite_score'] >= Decimal('80.00')
        assert match_res['is_recommended'] is True

    def test_interview_feedback_aggregation(self):
        user = User.objects.create_user(username="interviewer.deep.user", password="Password@123")
        emp = Employee.objects.create(
            user=user,
            employee_id="EMP-IV-01",
            first_name="Vivek",
            last_name="Kapoor",
            email="vivek.iv@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        sched = InterviewSchedule.objects.create(
            application=self.app,
            round_name="System Architecture & MLOps Deep-Dive",
            scheduled_start=timezone.now(),
            scheduled_end=timezone.now(),
            status="COMPLETED"
        )
        fb = InterviewFeedback.objects.create(
            interview=sched,
            interviewer=emp,
            technical_rating=5,
            communication_rating=4,
            problem_solving_rating=5,
            cultural_fit_rating=5,
            recommendation="STRONG_HIRE",
            key_strengths="Exceptional Kubernetes & PyTorch distributed training architecture knowledge",
            summary_comments="Definite hire for the core MLOps team."
        )
        assert fb.recommendation == "STRONG_HIRE"
        assert fb.technical_rating == 5

    def test_offer_letter_pipeline(self):
        offer = OfferLetter.objects.create(
            application=self.app,
            offer_code="OFFER-2026-AI-01",
            offered_designation="Lead MLOps Engineer",
            department=self.dept,
            offered_ctc_annual=Decimal('2300000.00'),
            joining_date=timezone.now().date(),
            offer_valid_until=timezone.now().date(),
            status="SENT"
        )
        assert offer.status == "SENT"
        offer.status = "ACCEPTED"
        offer.save()
        assert offer.status == "ACCEPTED"
