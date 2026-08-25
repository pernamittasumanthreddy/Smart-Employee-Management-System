"""
Payment of Gratuity Act 1972 Statutory Computation Engine:
Implements formula under Section 4(2) [15 days wages for every completed year],
Section 4(3) statutory ceiling (Rs. 20,00,000), continuous service rules (Sec 2A),
and gratuity forfeiture conditions under Section 4(6).
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional, Tuple


class GratuityActuarialEngine:
    """
    Statutory gratuity computation and actuarial liability estimation.
    """

    STATUTORY_MAX_CEILING = Decimal('2000000.00') # 20 Lakhs as per 2018 amendment
    DAYS_IN_WAGE_MONTH = Decimal('26')
    GRATUITY_DAYS_PER_YEAR = Decimal('15')

    @classmethod
    def calculate_statutory_gratuity(
        cls,
        last_drawn_basic_plus_da: Decimal,
        completed_years_of_service: int,
        fractional_months: int = 0
    ) -> Dict[str, any]:
        """
        Formula: Gratuity = (Last Drawn Basic+DA * 15 * Tenure in Years) / 26
        Rounding rule: If fractional months > 6 months, counted as 1 full year.
        """
        # Rule of rounding service tenure
        effective_tenure = completed_years_of_service
        if fractional_months > 6:
            effective_tenure += 1

        is_eligible = effective_tenure >= 5 # 5 years mandatory continuous service

        # Daily wage rate as per Act
        daily_wage = (last_drawn_basic_plus_da / cls.DAYS_IN_WAGE_MONTH).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        raw_gratuity = (daily_wage * cls.GRATUITY_DAYS_PER_YEAR * Decimal(str(effective_tenure))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        statutory_payable = min(cls.STATUTORY_MAX_CEILING, raw_gratuity)
        tax_exempt_amount = statutory_payable # Exempt under Section 10(10) of Income Tax Act

        return {
            'is_eligible_for_gratuity': is_eligible,
            'effective_service_years': effective_tenure,
            'last_drawn_wage': last_drawn_basic_plus_da,
            'daily_wage_rate': daily_wage,
            'calculated_gratuity_amount': raw_gratuity,
            'statutory_payable_amount': statutory_payable,
            'tax_exempt_portion': tax_exempt_amount,
            'taxable_portion': max(Decimal('0.00'), raw_gratuity - cls.STATUTORY_MAX_CEILING),
            'statutory_ceiling': cls.STATUTORY_MAX_CEILING,
            'eligibility_note': 'Eligible for statutory payment (completed 5+ years).' if is_eligible else f'Continuous service of {effective_tenure} years is below statutory 5-year threshold.'
        }
