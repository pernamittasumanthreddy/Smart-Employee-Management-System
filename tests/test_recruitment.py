import pytest
from decimal import Decimal
from django.utils import timezone
from apps.recruitment.models import JobRequisition, Candidate, JobApplication, OfferLetter
from apps.recruitment.matching import CandidateMatchingEngine
from apps.organization.models import Department

@pytest.mark.django_db
def test_candidate_matching_engine():
    candidate_skills = "Python, Django, PostgreSQL, Docker, AWS, Celery"
    req_skills = "Python, Django, AWS, Kubernetes"
    score = CandidateMatchingEngine.calculate_skill_match_score(candidate_skills, req_skills)
    assert score >= Decimal('70.00')

@pytest.mark.django_db
def test_job_application_lifecycle():
    dept, _ = Department.objects.get_or_create(name="Platform Engineering", code="ENG-PLT")
    req = JobRequisition.objects.create(
        title="Senior Backend Engineer",
        requisition_code="REQ-2026-099",
        department=dept,
        headcount=2,
        target_hire_date=timezone.now().date()
    )
    cand = Candidate.objects.create(
        first_name="Rohan",
        last_name="Verma",
        email="rohan.verma.test@example.com",
        phone="9876543210"
    )
    app = JobApplication.objects.create(
        job_requisition=req,
        candidate=cand,
        stage='APPLIED'
    )
    assert app.stage == 'APPLIED'
    app.stage = 'OFFER_EXTENDED'
    app.save()
    assert app.stage == 'OFFER_EXTENDED'
