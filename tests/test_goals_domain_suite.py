"""
Comprehensive Unit & Integration Test Suite for Objectives & Key Results (OKR) Domain Service.
"""

from decimal import Decimal
from datetime import datetime, date, timedelta
import pytest
from apps.goals.services.domain_engine import GoalsDomainEngine, GoalsDomainResult


class TestGoalsDomainEngine:
    def test_execute_core_workflow_success(self):
        """Verify successful domain workflow execution."""
        ctx = {'amount': 2500.00, 'reference': 'REF-2026-001', 'category': 'STANDARD'}
        res = GoalsDomainEngine.execute_core_workflow(
            entity_id=101,
            context_data=ctx,
            actor_user_id=1
        )
        assert res.is_success is True
        assert res.status == 'COMPLETED'
        assert res.metric_value == Decimal('2625.00')
        assert len(res.audit_tags) >= 3

    def test_execute_core_workflow_empty_context(self):
        """Verify error handling on empty context data."""
        res = GoalsDomainEngine.execute_core_workflow(
            entity_id=102,
            context_data={},
            actor_user_id=1
        )
        assert res.is_success is False
        assert res.status == 'ERROR'

    def test_validate_entity_state(self):
        """Verify state machine transition validation."""
        valid_states = ['DRAFT', 'SUBMITTED', 'APPROVED', 'REJECTED']
        assert GoalsDomainEngine.validate_entity_state(101, 'APPROVED', valid_states) is True
        assert GoalsDomainEngine.validate_entity_state(101, 'UNKNOWN_STATE', valid_states) is False

    def test_compute_summary_analytics(self):
        """Verify summary analytics calculations."""
        dataset = [
            {'id': 1, 'value': 100.0},
            {'id': 2, 'value': 200.0},
            {'id': 3, 'value': 300.0},
        ]
        res = GoalsDomainEngine.compute_summary_analytics(dataset)
        assert res['total_count'] == 3
        assert res['total_aggregate_value'] == Decimal('600.00')
        assert res['average_value'] == Decimal('200.00')
        assert res['status'] == 'HEALTHY'

    def test_compute_summary_analytics_empty(self):
        """Verify analytics on empty dataset."""
        res = GoalsDomainEngine.compute_summary_analytics([])
        assert res['total_count'] == 0
        assert res['status'] == 'EMPTY'
