"""
Unit Tests for Statutory Compliance Validator and Legal Rule Checker.
"""

from decimal import Decimal
import pytest
from apps.compliance.services.statutory_validator import StatutoryComplianceValidator


class TestStatutoryComplianceValidator:
    def test_minimum_wages_compliance_pass(self):
        violations = StatutoryComplianceValidator.validate_minimum_wages(
            state='KARNATAKA',
            skill_category='SKILLED',
            monthly_basic_plus_da=Decimal('25000.00')
        )
        assert len(violations) == 0

    def test_minimum_wages_violation_detect(self):
        violations = StatutoryComplianceValidator.validate_minimum_wages(
            state='KARNATAKA',
            skill_category='SKILLED',
            monthly_basic_plus_da=Decimal('12000.00')
        )
        assert len(violations) == 1
        assert violations[0].statute_code == 'MWA_1948_SEC12'
        assert violations[0].severity == 'CRITICAL'

    def test_work_hours_ceiling_violation(self):
        violations = StatutoryComplianceValidator.validate_work_hours_and_overtime(
            daily_hours=Decimal('10.5'),
            weekly_hours=Decimal('54.0'),
            consecutive_days=7,
            interval_rest_minutes=15
        )
        assert len(violations) >= 3 # Daily ceiling, weekly ceiling, consecutive days, rest interval

    def test_maternity_benefit_sanction_check(self):
        violations = StatutoryComplianceValidator.validate_maternity_benefit_compliance(
            employee_gender='FEMALE',
            days_worked_past_12_months=120,
            is_maternity_requested=True,
            approved_leave_weeks=18
        )
        assert len(violations) == 1
        assert violations[0].statute_code == 'MBA_2017_AMENDMENT'
