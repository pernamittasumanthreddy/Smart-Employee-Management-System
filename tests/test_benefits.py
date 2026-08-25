import pytest
from decimal import Decimal
from django.utils import timezone
from apps.benefits.models import InsurancePolicy, EmployeeInsuranceEnrollment, InsuranceClaim
from apps.employees.models import Employee

@pytest.mark.django_db
def test_benefits_and_claims():
    policy = InsurancePolicy.objects.create(
        name="HDFC ERGO Health Suraksha Floater",
        policy_number="HDFC-POL-9921",
        sum_insured=Decimal('500000.00'),
        start_date=timezone.now().date(),
        end_date=timezone.now().date()
    )
    assert policy.sum_insured == Decimal('500000.00')
