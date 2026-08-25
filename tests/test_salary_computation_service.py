"""
Unit Tests for Salary Slip Formula Generation Engine.
"""

from decimal import Decimal
import pytest
from apps.payroll.services.salary_slip_generator import SalaryCalculationEngine


class TestSalaryCalculationEngine:
    def test_epf_contributions_with_ceiling(self):
        """EPF calculations capped at statutory Rs. 15,000 ceiling."""
        res = SalaryCalculationEngine.calculate_epf_contributions(Decimal('45000.00'), cap_at_statutory_ceiling=True)
        assert res['epf_employee'] == Decimal('1800.00') # 12% of 15,000
        assert res['eps_employer'] == Decimal('1250.00') # 8.33% capped at 1250
        assert res['epf_employer'] == Decimal('550.00')  # 1800 - 1250

    def test_epf_contributions_without_ceiling(self):
        """EPF calculations on actual basic salary without ceiling."""
        res = SalaryCalculationEngine.calculate_epf_contributions(Decimal('50000.00'), cap_at_statutory_ceiling=False)
        assert res['epf_employee'] == Decimal('6000.00') # 12% of 50,000

    def test_esi_applicable_under_21k(self):
        emp_esi, empr_esi = SalaryCalculationEngine.calculate_esi_contributions(Decimal('18000.00'))
        assert emp_esi == Decimal('135.00') # 0.75% of 18,000
        assert empr_esi == Decimal('585.00') # 3.25% of 18,000

    def test_esi_exempt_above_21k(self):
        emp_esi, empr_esi = SalaryCalculationEngine.calculate_esi_contributions(Decimal('45000.00'))
        assert emp_esi == Decimal('0.00')
        assert empr_esi == Decimal('0.00')

    def test_gratuity_provision(self):
        basic = Decimal('52000.00')
        prov = SalaryCalculationEngine.calculate_gratuity_provision(basic)
        # (52,000 * 15 / 26) / 12 = 30,000 / 12 = 2500.00
        assert prov == Decimal('2500.00')

    def test_full_pay_breakdown_matches_ctc(self):
        monthly_ctc = Decimal('100000.00')
        breakdown = SalaryCalculationEngine.generate_full_pay_breakdown(monthly_ctc=monthly_ctc)
        assert breakdown.total_cost_to_company == monthly_ctc
        assert breakdown.gross_earnings > breakdown.net_take_home_pay
        assert breakdown.net_take_home_pay > Decimal('0.00')
