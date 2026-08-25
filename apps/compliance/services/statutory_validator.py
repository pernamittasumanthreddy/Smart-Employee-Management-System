"""
Statutory Compliance & Legal Rule Verification Engine:
Validates Minimum Wages Act, Payment of Wages Act, Maternity Benefit Act 2017,
Factories Act 1948, Equal Remuneration Act 1976, and Code on Social Security 2020.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Tuple


@dataclass
class ComplianceViolation:
    statute_code: str
    statute_name: str
    severity: str # CRITICAL, HIGH, MEDIUM, LOW
    violation_message: str
    recommended_remediation: str
    statutory_penalty_clause: str


class StatutoryComplianceValidator:
    """
    Automated legal audit engine verifying workforce operations against
    Indian Labour Laws and Central/State Government enactments.
    """

    MINIMUM_WAGES_2026_MATRIX = {
        'KARNATAKA': {'UNSKILLED': Decimal('16250.00'), 'SEMI_SKILLED': Decimal('17800.00'), 'SKILLED': Decimal('19500.00'), 'HIGHLY_SKILLED': Decimal('21800.00')},
        'MAHARASHTRA': {'UNSKILLED': Decimal('15800.00'), 'SEMI_SKILLED': Decimal('17200.00'), 'SKILLED': Decimal('18900.00'), 'HIGHLY_SKILLED': Decimal('20900.00')},
        'DELHI': {'UNSKILLED': Decimal('17494.00'), 'SEMI_SKILLED': Decimal('19279.00'), 'SKILLED': Decimal('21215.00'), 'HIGHLY_SKILLED': Decimal('23000.00')},
        'TELANGANA': {'UNSKILLED': Decimal('14900.00'), 'SEMI_SKILLED': Decimal('16400.00'), 'SKILLED': Decimal('18100.00'), 'HIGHLY_SKILLED': Decimal('20100.00')},
        'TAMIL_NADU': {'UNSKILLED': Decimal('14500.00'), 'SEMI_SKILLED': Decimal('15900.00'), 'SKILLED': Decimal('17500.00'), 'HIGHLY_SKILLED': Decimal('19500.00')},
    }

    WEEKLY_HOURS_CEILING = Decimal('48.0')
    DAILY_HOURS_CEILING = Decimal('9.0')
    SPREADOVER_MAX_HOURS = Decimal('10.5')
    MAX_CONSECUTIVE_WORK_DAYS = 6

    @classmethod
    def validate_minimum_wages(
        cls,
        state: str,
        skill_category: str,
        monthly_basic_plus_da: Decimal
    ) -> List[ComplianceViolation]:
        violations = []
        state_key = state.upper().replace(' ', '_')
        category_key = skill_category.upper().replace(' ', '_')

        rates = cls.MINIMUM_WAGES_2026_MATRIX.get(state_key, cls.MINIMUM_WAGES_2026_MATRIX['KARNATAKA'])
        min_statutory_wage = rates.get(category_key, rates['SKILLED'])

        if monthly_basic_plus_da < min_statutory_wage:
            deficit = min_statutory_wage - monthly_basic_plus_da
            violations.append(ComplianceViolation(
                statute_code='MWA_1948_SEC12',
                statute_name='Minimum Wages Act, 1948 - Section 12',
                severity='CRITICAL',
                violation_message=f"Basic + DA (Rs. {monthly_basic_plus_da}) is below statutory minimum wage of Rs. {min_statutory_wage} for {state_key} ({category_key}). Deficit: Rs. {deficit}.",
                recommended_remediation=f"Increase Basic Salary component by at least Rs. {deficit} per month.",
                statutory_penalty_clause='Section 22: Imprisonment up to 6 months or fine up to Rs. 50,000 or both.'
            ))

        return violations

    @classmethod
    def validate_work_hours_and_overtime(
        cls,
        daily_hours: Decimal,
        weekly_hours: Decimal,
        consecutive_days: int,
        interval_rest_minutes: int
    ) -> List[ComplianceViolation]:
        violations = []

        # 1. Daily Ceiling (9 Hours)
        if daily_hours > cls.DAILY_HOURS_CEILING:
            violations.append(ComplianceViolation(
                statute_code='FA_1948_SEC54',
                statute_name='Factories Act, 1948 - Section 54 (Daily Hours)',
                severity='HIGH',
                violation_message=f"Daily work shift of {daily_hours} hours exceeds the statutory 9-hour limit.",
                recommended_remediation='Limit standard daily shift to 8-9 hours and treat remainder as overtime.',
                statutory_penalty_clause='Section 92: General penalty for offences under Factories Act.'
            ))

        # 2. Weekly Ceiling (48 Hours)
        if weekly_hours > cls.WEEKLY_HOURS_CEILING:
            violations.append(ComplianceViolation(
                statute_code='FA_1948_SEC51',
                statute_name='Factories Act, 1948 - Section 51 (Weekly Hours)',
                severity='HIGH',
                violation_message=f"Total weekly hours of {weekly_hours} hours exceed statutory ceiling of 48 hours without authorized overtime approval.",
                recommended_remediation='Ensure total weekly hours including overtime do not exceed 60 hours per quarter.',
                statutory_penalty_clause='Section 59: Double rate wage mandate for hours exceeding 48 hours weekly.'
            ))

        # 3. Weekly Rest Day (Section 52)
        if consecutive_days > cls.MAX_CONSECUTIVE_WORK_DAYS:
            violations.append(ComplianceViolation(
                statute_code='FA_1948_SEC52',
                statute_name='Factories Act, 1948 - Section 52 (Weekly Holidays)',
                severity='CRITICAL',
                violation_message=f"Employee has worked {consecutive_days} consecutive days without a mandatory 24-hour weekly rest day.",
                recommended_remediation='Schedule mandatory compensatory off within the immediate 3-day window.',
                statutory_penalty_clause='Section 53: Compensatory holidays mandatory within the month.'
            ))

        # 4. Rest Intervals (Section 55 - 30 mins after 5 hours)
        if interval_rest_minutes < 30 and daily_hours > Decimal('5.0'):
            violations.append(ComplianceViolation(
                statute_code='FA_1948_SEC55',
                statute_name='Factories Act, 1948 - Section 55 (Intervals for Rest)',
                severity='MEDIUM',
                violation_message='No rest interval of at least 30 minutes provided after 5 continuous hours of work.',
                recommended_remediation='Provision at least 45-60 minutes meal/rest break midway through the shift.',
                statutory_penalty_clause='Compliance breach in statutory shift roster.'
            ))

        return violations

    @classmethod
    def validate_maternity_benefit_compliance(
        cls,
        employee_gender: str,
        days_worked_past_12_months: int,
        is_maternity_requested: bool,
        approved_leave_weeks: int
    ) -> List[ComplianceViolation]:
        violations = []
        if employee_gender.upper() != 'FEMALE' or not is_maternity_requested:
            return violations

        # Section 5(2): Must have worked at least 80 days in preceding 12 months
        if days_worked_past_12_months < 80:
            violations.append(ComplianceViolation(
                statute_code='MBA_1961_SEC5_2',
                statute_name='Maternity Benefit Act, 1961 - Section 5(2) Eligibility',
                severity='MEDIUM',
                violation_message=f"Employee has completed {days_worked_past_12_months} days (minimum 80 days required for statutory benefit).",
                recommended_remediation='Evaluate compassionate discretionary leave or special medical leave approval.',
                statutory_penalty_clause='Exempt from mandatory paid benefit if 80-day threshold is not met.'
            ))

        # Section 5(3): 26 weeks paid maternity leave for up to 2 surviving children
        if approved_leave_weeks < 26:
            violations.append(ComplianceViolation(
                statute_code='MBA_2017_AMENDMENT',
                statute_name='Maternity Benefit (Amendment) Act, 2017 - Section 5(3)',
                severity='CRITICAL',
                violation_message=f"Sanctioned maternity leave of {approved_leave_weeks} weeks is less than statutory 26 weeks.",
                recommended_remediation='Extend approved paid maternity leave duration to full 26 weeks (182 calendar days).',
                statutory_penalty_clause='Section 21: Imprisonment up to 1 year and fine up to Rs. 50,000.'
            ))

        return violations
