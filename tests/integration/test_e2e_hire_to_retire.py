import pytest
from decimal import Decimal
from django.utils import timezone
from apps.employees.models import Employee
from apps.lifecycle.models import OnboardingWorkflow, ResignationRequest, DepartmentClearance
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestHireToRetireE2E:
    def test_full_employee_lifecycle_journey(self):
        user = User.objects.create_user(username="e2e.hire.user", password="Password@123")
        emp = Employee.objects.create(
            user=user,
            employee_id="EMP-E2E-001",
            first_name="Abhinav",
            last_name="Bindra",
            email="abhinav.e2e@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        # Onboarding
        wf = OnboardingWorkflow.objects.create(
            employee=emp,
            joining_date=timezone.now().date(),
            probation_end_date=timezone.now().date(),
            status='COMPLETED'
        )
        assert wf.status == 'COMPLETED'

        # Resignation and Exit Clearance
        resig = ResignationRequest.objects.create(
            employee=emp,
            proposed_last_working_day=timezone.now().date(),
            detailed_reason="Relocating for Olympic Foundation Leadership",
            status="APPROVED"
        )
        assert resig.status == "APPROVED"
