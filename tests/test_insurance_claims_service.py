"""
Unit Tests for Group Health Insurance Claims Adjudicator.
"""

from decimal import Decimal
import pytest
from apps.benefits.services.insurance_claim_engine import InsuranceClaimEngine


class TestInsuranceClaimEngine:
    def test_standard_claim_adjudication(self):
        res = InsuranceClaimEngine.adjudicate_claim(
            claim_id='CLM-2026-881',
            emp_id=101,
            patient_name='Rahul K',
            is_parent=False,
            sum_insured=Decimal('500000.00'),
            hospital_bill=Decimal('120000.00'),
            room_rent_per_day=Decimal('4000.00'), # Below 1% of 5L (5000/day)
            hospitalization_days=4,
            non_medical_charges=Decimal('5000.00')
        )
        assert res.claim_status == 'APPROVED'
        assert res.room_rent_deduction == Decimal('0.00')
        assert res.final_settled_amount == Decimal('115000.00') # 120k - 5k

    def test_parental_copay_deduction(self):
        res = InsuranceClaimEngine.adjudicate_claim(
            claim_id='CLM-2026-882',
            emp_id=102,
            patient_name='Father of Emp',
            is_parent=True, # 10% co-pay
            sum_insured=Decimal('500000.00'),
            hospital_bill=Decimal('100000.00'),
            room_rent_per_day=Decimal('3000.00'),
            hospitalization_days=3,
            non_medical_charges=Decimal('0.00')
        )
        assert res.co_pay_deduction == Decimal('10000.00') # 10% of 100k
        assert res.final_settled_amount == Decimal('90000.00')
