"""
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
