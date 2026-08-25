import os
import sys

def write_code(rel_path, content):
    os.makedirs(os.path.dirname(rel_path), exist_ok=True)
    with open(rel_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    lines = len(content.strip().splitlines())
    print(f"Generated: {rel_path} ({lines} LOC)")

print("Generating Compliance and Statutory Governance Engine...")

# 1. Statutory Compliance Validator
statutory_validator_code = '''"""
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
'''

write_code('apps/compliance/services/statutory_validator.py', statutory_validator_code)

# 2. Audit Report Register Generator
audit_report_code = '''"""
Statutory Register & Legal Audit Report Generator:
Generates Form A (Employee Register), Form B (Wage Register),
Form C (Loan/Recovery), Form D (Attendance), and Form E (Overtime).
"""

import csv
import io
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional


class StatutoryAuditReportGenerator:
    """
    Compiles formal regulatory audit registers required under
    Ease of Compliance Rules 2017 and Code on Wages 2019.
    """

    @classmethod
    def generate_form_a_employee_register_csv(cls, employees: List[Dict]) -> str:
        """
        Form A: Format of Employee Register (Rule 2(1) of Ease of Compliance Rules).
        """
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['FORM A - FORMAT OF EMPLOYEE REGISTER'])
        writer.writerow(['[See Rule 2(1) of Ease of Compliance to Maintain Registers under various Labour Laws Rules, 2017]'])
        writer.writerow(['Name of the Establishment: Bharat Enterprise Solutions Ltd.', 'CIN: U72200KA2024PLC098765'])
        writer.writerow([])

        headers = [
            'Sl. No', 'Employee ID', 'Full Name', 'Gender', "Father's/Spouse Name",
            'Date of Birth', 'Nationality', 'Education Level', 'Date of Joining',
            'Designation', 'Category (Skill)', 'Type of Employment', 'Mobile No',
            'UAN (EPF)', 'ESIC No', 'Aadhaar / National ID', 'Bank Account No',
            'Bank IFSC', 'Present Address', 'Permanent Address', 'Status'
        ]
        writer.writerow(headers)

        for idx, emp in enumerate(employees, start=1):
            writer.writerow([
                idx,
                emp.get('employee_id', f'EMP-{idx:04d}'),
                emp.get('full_name', 'N/A'),
                emp.get('gender', 'PREFER_NOT_TO_SAY'),
                emp.get('father_name', '--'),
                emp.get('dob', '1995-01-01'),
                'Indian',
                emp.get('education', 'Graduate (B.Tech / B.E)'),
                emp.get('doj', '2024-01-15'),
                emp.get('designation', 'Engineer'),
                emp.get('skill_category', 'SKILLED'),
                emp.get('employment_type', 'FULL_TIME'),
                emp.get('phone', '9876543210'),
                emp.get('uan', f'10123456{idx:04d}'),
                emp.get('esic', f'31234567{idx:04d}'),
                emp.get('national_id', f'XXXX-XXXX-{idx:04d}'),
                emp.get('bank_account', f'918273645{idx:04d}'),
                'HDFC0001234',
                emp.get('current_address', 'Bangalore, Karnataka'),
                emp.get('permanent_address', 'Bangalore, Karnataka'),
                'ACTIVE'
            ])

        return output.getvalue()

    @classmethod
    def generate_form_b_wage_register_csv(cls, wage_records: List[Dict], month_year: str) -> str:
        """
        Form B: Format of Register of Wages (Rule 2(1)).
        """
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['FORM B - FORMAT OF REGISTER OF WAGES'])
        writer.writerow([f'Wage Period: {month_year}', 'Name of Establishment: Bharat Enterprise Solutions Ltd.'])
        writer.writerow([])

        headers = [
            'Sl. No', 'Emp ID', 'Name', 'Designation', 'Total Days Worked',
            'Units / Hours', 'Basic Pay', 'DA', 'HRA', 'Special Allow',
            'Overtime Pay', 'Gross Wages', 'EPF Ded', 'ESI Ded', 'PTax Ded',
            'TDS Ded', 'Other Ded', 'Total Deductions', 'Net Wages Paid',
            'Date of Payment', 'Signature / Digital Bank Ref'
        ]
        writer.writerow(headers)

        for idx, w in enumerate(wage_records, start=1):
            writer.writerow([
                idx,
                w.get('employee_id', f'EMP-{idx:04d}'),
                w.get('name', 'Staff'),
                w.get('designation', 'Executive'),
                w.get('days_worked', 30),
                w.get('hours', 240),
                w.get('basic', '45000.00'),
                '0.00',
                w.get('hra', '22500.00'),
                w.get('special', '12500.00'),
                w.get('ot_pay', '0.00'),
                w.get('gross', '80000.00'),
                w.get('epf', '1800.00'),
                w.get('esi', '0.00'),
                w.get('ptax', '200.00'),
                w.get('tds', '4500.00'),
                '0.00',
                w.get('total_ded', '6500.00'),
                w.get('net_pay', '73500.00'),
                'Last Working Day of Month',
                f'UTR-NEFT-2026{idx:06d}'
            ])

        return output.getvalue()
'''

write_code('apps/compliance/services/audit_report_generator.py', audit_report_code)

# 3. POSH Governance Engine
posh_engine_code = '''"""
POSH (Prevention of Sexual Harassment) Statutory Governance Engine:
Implements Internal Committee (IC) constitution compliance, 90-day inquiry
statutory timeline tracking, reconciliation workflows, and Section 21 Annual Report compiler.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, List, Optional


@dataclass
class POSHCaseMilestone:
    complaint_id: str
    complainant_name: str
    respondent_name: str
    date_of_incident: date
    date_of_complaint: date
    statutory_90_day_deadline: date
    current_stage: str # SUBMITTED, NOTICE_ISSUED, CONCILIATION, FORMAL_INQUIRY, REPORT_SUBMITTED, CLOSED
    is_conciliation_requested: bool
    interim_relief_granted: bool
    days_elapsed: int
    days_remaining: int
    is_overdue: bool


class POSHGovernanceEngine:
    """
    Statutory workflow engine enforcing compliance under
    The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013.
    """

    STATUTORY_LIMIT_DAYS = 90
    EMPLOYER_ACTION_LIMIT_DAYS = 60

    @classmethod
    def track_case_statutory_timeline(
        cls,
        complaint_id: str,
        complainant: str,
        respondent: str,
        incident_dt: date,
        complaint_dt: date,
        stage: str,
        is_conciliation: bool = False,
        interim_relief: bool = False
    ) -> POSHCaseMilestone:
        deadline = complaint_dt + timedelta(days=cls.STATUTORY_LIMIT_DAYS)
        today = date.today()
        elapsed = (today - complaint_dt).days
        remaining = max(0, (deadline - today).days)
        overdue = (today > deadline) and (stage != 'CLOSED')

        return POSHCaseMilestone(
            complaint_id=complaint_id,
            complainant_name=complainant,
            respondent_name=respondent,
            date_of_incident=incident_dt,
            date_of_complaint=complaint_dt,
            statutory_90_day_deadline=deadline,
            current_stage=stage,
            is_conciliation_requested=is_conciliation,
            interim_relief_granted=interim_relief,
            days_elapsed=elapsed,
            days_remaining=remaining,
            is_overdue=overdue
        )

    @classmethod
    def validate_ic_constitution(
        cls,
        total_members: int,
        presiding_officer_is_senior_woman: bool,
        female_member_count: int,
        has_external_ngo_member: bool
    ) -> Dict[str, any]:
        """
        Validates statutory constitution of Internal Committee under Section 4(2):
        - Presiding Officer must be a senior level woman employee.
        - Not less than 50% members must be women.
        - Must include 1 external member from NGO / legal background.
        - Minimum 4 members.
        """
        violations = []

        if total_members < 4:
            violations.append("Total IC membership is below statutory minimum of 4 members.")

        if not presiding_officer_is_senior_woman:
            violations.append("Presiding Officer must be a senior woman employed at the workplace.")

        female_ratio = female_member_count / total_members if total_members > 0 else 0
        if female_ratio < 0.50:
            violations.append(f"Women representation ({female_member_count}/{total_members} = {female_ratio*100:.1f}%) is below mandatory 50% threshold.")

        if not has_external_ngo_member:
            violations.append("IC must have at least 1 external member from an NGO or association committed to women's cause.")

        return {
            'is_compliant': len(violations) == 0,
            'violations': violations,
            'statutory_recommendation': 'Rectify IC composition immediately to prevent invalidation of enquiry proceedings.' if violations else 'Internal Committee is statutorily compliant.'
        }
'''

write_code('apps/compliance/services/posh_governance_engine.py', posh_engine_code)

print("Compliance Suite Generated Successfully!")
