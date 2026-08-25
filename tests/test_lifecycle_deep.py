import pytest
from django.utils import timezone
from apps.lifecycle.models import OnboardingWorkflow, OnboardingTask, ProbationReview, ResignationRequest, DepartmentClearance, ExperienceCertificate
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestLifecycleDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="lifecycle.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-LC-DEEP-01",
            first_name="Siddharth",
            last_name="Menon",
            email="siddharth.m@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )

    def test_onboarding_task_lifecycle(self):
        wf = OnboardingWorkflow.objects.create(
            employee=self.emp,
            joining_date=timezone.now().date(),
            probation_end_date=timezone.now().date(),
            status="INITIATED"
        )
        t1 = OnboardingTask.objects.create(
            workflow=wf,
            title="Allocate MacBook Pro M3 & YubiKey",
            category="IT_SETUP",
            due_date=timezone.now().date(),
            is_completed=True
        )
        t2 = OnboardingTask.objects.create(
            workflow=wf,
            title="Complete Code of Conduct & POSH Training",
            category="TRAINING",
            due_date=timezone.now().date(),
            is_completed=False
        )
        assert wf.tasks.count() == 2
        assert t1.is_completed is True

    def test_probation_review_regularization(self):
        rev = ProbationReview.objects.create(
            employee=self.emp,
            reviewer=self.emp,
            performance_score=5,
            culture_fit_score=5,
            attendance_score=5,
            decision="CONFIRM",
            manager_feedback="Exceeded all onboarding sprint deliverables.",
            is_approved_by_hr=True
        )
        assert rev.decision == "CONFIRM"
        assert rev.is_approved_by_hr is True

    def test_exit_clearance_signoffs(self):
        resig = ResignationRequest.objects.create(
            employee=self.emp,
            resignation_date=timezone.now().date(),
            proposed_last_working_day=timezone.now().date(),
            reason_category="BETTER_OPPORTUNITY",
            detailed_reason="Relocating for executive leadership role.",
            status="CLEARANCE"
        )
        cl_it = DepartmentClearance.objects.create(
            resignation=resig,
            department_name="IT",
            is_cleared=True,
            pending_items="None (Laptop & Access Card Returned)"
        )
        cl_fin = DepartmentClearance.objects.create(
            resignation=resig,
            department_name="FINANCE",
            is_cleared=True,
            pending_items="None (No Pending Travel Advances)"
        )
        assert resig.clearances.count() == 2
        assert cl_it.is_cleared is True
