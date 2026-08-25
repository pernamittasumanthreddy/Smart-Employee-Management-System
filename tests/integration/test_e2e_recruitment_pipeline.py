import pytest
from decimal import Decimal
from django.utils import timezone
from apps.recruitment.models import JobRequisition, Candidate, JobApplication, InterviewSchedule, OfferLetter
from apps.recruitment.matching import CandidateMatchingEngine
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestRecruitmentPipelineE2E:
    def test_job_application_to_offer_acceptance(self):
        req = JobRequisition.objects.create(
            title="Principal Distributed Systems Architect",
            requisition_code="REQ-E2E-ARCH-01",
            headcount=1,
            min_experience_years=Decimal('8.0'),
            max_experience_years=Decimal('15.0'),
            budget_min=Decimal('3000000.00'),
            budget_max=Decimal('4500000.00'),
            required_skills="Go, Rust, Distributed Systems, Kubernetes, Kafka",
            target_hire_date=timezone.now().date()
        )
        cand = Candidate.objects.create(
            first_name="Neeraj",
            last_name="Chopra",
            email="neeraj.systems@example.com",
            phone="+91 99999 88888",
            total_experience_years=Decimal('10.0'),
            current_ctc=Decimal('2800000.00'),
            expected_ctc=Decimal('4000000.00'),
            notice_period_days=30,
            skills_summary="Go, Rust, Distributed Systems, Kubernetes, Kafka, Raft Consensus"
        )
        match_res = CandidateMatchingEngine.calculate_overall_match_index(cand, req)
        assert match_res['composite_score'] >= Decimal('80.00')

        app = JobApplication.objects.create(job_requisition=req, candidate=cand, stage="OFFER", match_score_percentage=95)
        offer = OfferLetter.objects.create(
            application=app,
            offer_code="OFFER-E2E-ARCH-01",
            offered_designation="Principal Distributed Systems Architect",
            offered_ctc_annual=Decimal('4200000.00'),
            joining_date=timezone.now().date(),
            offer_valid_until=timezone.now().date(),
            status="ACCEPTED"
        )
        assert offer.status == "ACCEPTED"
