import pytest
from decimal import Decimal
from django.utils import timezone
from apps.benefits.models import InsurancePolicy, EmployeeInsuranceEnrollment, InsuranceClaim, FlexibleBenefitPlan
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestBenefitsDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="ben.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-BEN-DEEP-01",
            first_name="Meera",
            last_name="Nair",
            email="meera.ben@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.pol = InsurancePolicy.objects.create(
            name="Executive Comprehensive GMC Floater",
            policy_number="HDFC-GMC-2026-X",
            provider_name="HDFC ERGO General Insurance",
            policy_type="GMC",
            sum_insured=Decimal('750000.00'),
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            tpa_name="Paramount Health Services TPA",
            is_active=True
        )

    def test_insurance_enrollment_and_claim(self):
        enr = EmployeeInsuranceEnrollment.objects.create(
            employee=self.emp,
            policy=self.pol,
            card_number="HDFC-CARD-9912",
            enrolled_date=timezone.now().date(),
            sum_insured_allocated=Decimal('750000.00')
        )
        claim = InsuranceClaim.objects.create(
            enrollment=enr,
            claim_number="CLM-2026-9012",
            patient_name="Meera Nair",
            relationship="SELF",
            hospital_name="Apollo Hospitals Bengaluru",
            admission_date=timezone.now().date(),
            discharge_date=timezone.now().date(),
            claimed_amount=Decimal('45000.00'),
            approved_amount=Decimal('42000.00'),
            status="APPROVED"
        )
        assert enr.card_number == "HDFC-CARD-9912"
        assert claim.status == "APPROVED"
        assert claim.approved_amount == Decimal('42000.00')
