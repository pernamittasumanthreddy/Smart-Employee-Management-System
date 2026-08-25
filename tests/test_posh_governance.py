"""
Unit Tests for POSH Governance and Statutory 90-Day Timeline Monitor.
"""

from datetime import date, timedelta
import pytest
from apps.compliance.services.posh_governance_engine import POSHGovernanceEngine


class TestPOSHGovernanceEngine:
    def test_statutory_timeline_within_deadline(self):
        complaint_dt = date.today() - timedelta(days=30)
        res = POSHGovernanceEngine.track_case_statutory_timeline(
            complaint_id='POSH-2026-001',
            complainant='Employee A',
            respondent='Employee B',
            incident_dt=complaint_dt - timedelta(days=5),
            complaint_dt=complaint_dt,
            stage='FORMAL_INQUIRY'
        )
        assert not res.is_overdue
        assert res.days_elapsed == 30
        assert res.days_remaining == 60

    def test_statutory_timeline_overdue(self):
        complaint_dt = date.today() - timedelta(days=95)
        res = POSHGovernanceEngine.track_case_statutory_timeline(
            complaint_id='POSH-2026-002',
            complainant='Employee X',
            respondent='Employee Y',
            incident_dt=complaint_dt - timedelta(days=10),
            complaint_dt=complaint_dt,
            stage='FORMAL_INQUIRY'
        )
        assert res.is_overdue
        assert res.days_remaining == 0

    def test_ic_constitution_compliance_pass(self):
        res = POSHGovernanceEngine.validate_ic_constitution(
            total_members=5,
            presiding_officer_is_senior_woman=True,
            female_member_count=3,
            has_external_ngo_member=True
        )
        assert res['is_compliant']
        assert len(res['violations']) == 0

    def test_ic_constitution_invalid_presiding_officer(self):
        res = POSHGovernanceEngine.validate_ic_constitution(
            total_members=4,
            presiding_officer_is_senior_woman=False,
            female_member_count=1,
            has_external_ngo_member=False
        )
        assert not res['is_compliant']
        assert len(res['violations']) >= 3
