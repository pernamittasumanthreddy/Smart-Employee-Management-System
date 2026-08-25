"""
Unit Tests for Gratuity Actuarial Calculation Engine.
"""

from decimal import Decimal
import pytest
from apps.compliance.services.gratuity_actuarial_engine import GratuityActuarialEngine


class TestGratuityActuarialEngine:
    def test_gratuity_tenure_rounding(self):
        """Tenure of 5 years 8 months rounds to 6 years."""
        res = GratuityActuarialEngine.calculate_statutory_gratuity(
            last_drawn_basic_plus_da=Decimal('52000.00'),
            completed_years_of_service=5,
            fractional_months=8
        )
        assert res['is_eligible_for_gratuity']
        assert res['effective_service_years'] == 6
        # Daily wage = 52,000 / 26 = 2000
        # Gratuity = 2000 * 15 * 6 = 1,80,000
        assert res['calculated_gratuity_amount'] == Decimal('180000.00')

    def test_gratuity_ineligible_under_5_years(self):
        res = GratuityActuarialEngine.calculate_statutory_gratuity(
            last_drawn_basic_plus_da=Decimal('50000.00'),
            completed_years_of_service=3,
            fractional_months=2
        )
        assert not res['is_eligible_for_gratuity']

    def test_gratuity_capped_at_20_lakhs(self):
        res = GratuityActuarialEngine.calculate_statutory_gratuity(
            last_drawn_basic_plus_da=Decimal('260000.00'), # 10k/day
            completed_years_of_service=25
        )
        # 10,000 * 15 * 25 = 37,50,000 -> Should cap at 20,00,000
        assert res['statutory_payable_amount'] == Decimal('2000000.00')
        assert res['taxable_portion'] == Decimal('1750000.00')
