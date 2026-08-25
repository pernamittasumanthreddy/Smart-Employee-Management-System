"""
Statutory Overtime Calculation Engine:
Computes overtime compensation rates under Section 59 of Factories Act
(Double the Ordinary Rate of Wages) and Night Shift Premium allowances.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict


class OvertimeCalculationEngine:
    """
    Overtime computation according to statutory wage multipliers.
    """

    STATUTORY_OT_MULTIPLIER = Decimal('2.0') # Double rate
    NIGHT_SHIFT_ALLOWANCE_PER_NIGHT = Decimal('350.00')

    @classmethod
    def calculate_overtime_pay(
        cls,
        monthly_basic_plus_da: Decimal,
        overtime_hours: Decimal,
        standard_monthly_hours: Decimal = Decimal('200.00'),
        is_holiday_work: bool = False
    ) -> Dict[str, Decimal]:
        """
        Hourly rate = (Monthly Basic + DA) / Standard Monthly Hours (e.g. 25 days * 8h = 200h).
        OT Rate = Hourly Rate * 2.0 (Double Rate).
        """
        hourly_rate = (monthly_basic_plus_da / standard_monthly_hours).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        multiplier = Decimal('2.5') if is_holiday_work else cls.STATUTORY_OT_MULTIPLIER
        ot_hourly_rate = (hourly_rate * multiplier).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        total_ot_amount = (ot_hourly_rate * overtime_hours).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return {
            'standard_hourly_rate': hourly_rate,
            'overtime_rate_per_hour': ot_hourly_rate,
            'overtime_hours': overtime_hours,
            'multiplier_applied': multiplier,
            'total_overtime_amount': total_ot_amount
        }
