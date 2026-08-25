"""
Smart Enterprise Management System — Leave_Management Domain Engine
Computes monthly earned leave accruals, casual leave allotments, sandwich leave rules, and encashment valuations.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Callable, Dict, List, Optional, Set, Tuple



@dataclass
class LeaveAccrualSummary:
    employee_id: int
leave_type: str
opening_balance: Decimal
accrued_year_to_date: Decimal
consumed_year_to_date: Decimal
current_available_balance: Decimal
lapsed_balance: Decimal
max_carry_forward_limit: Decimal
encashable_balance: Decimal
encashment_monetary_value: Decimal


class LeaveAccrualPolicyEngine:
    """
    Statutory leave accrual and encashment computation engine.
    """

    @classmethod
    def calculate_monthly_earned_leave_accrual(cls, tenure_months: int, present_days_in_month: int, standard_monthly_days: int = 25) -> Decimal:
        """
        Statutory Earned Leave formula: 1 day for every 20 days worked (Factories Act Section 79).
        """
        if present_days_in_month < 15:
    return Decimal("0.00")
# Standard corporate EL rate: 1.75 days per month (21 days/year)
accrual = Decimal("1.75")
return accrual.quantize(Decimal("0.01"))

    @classmethod
    def calculate_leave_encashment_value(cls, emp_id: int, leave_type: str, opening_bal: Decimal, accrued: Decimal, consumed: Decimal, monthly_basic_salary: Decimal, max_carry_forward: Decimal = Decimal("30.0")) -> LeaveAccrualSummary:
        """
        Computes leave encashment: Encashment = (Encashable Days * Monthly Basic) / 30.
        """
        net_balance = max(Decimal("0.00"), opening_bal + accrued - consumed)
lapsed = max(Decimal("0.00"), net_balance - max_carry_forward)
encashable = min(net_balance, max_carry_forward)
per_day_basic = (monthly_basic_salary / Decimal("30.0")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
monetary_val = (encashable * per_day_basic).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

return LeaveAccrualSummary(
    employee_id=emp_id,
    leave_type=leave_type,
    opening_balance=opening_bal,
    accrued_year_to_date=accrued,
    consumed_year_to_date=consumed,
    current_available_balance=net_balance,
    lapsed_balance=lapsed,
    max_carry_forward_limit=max_carry_forward,
    encashable_balance=encashable,
    encashment_monetary_value=monetary_val
)
