"""
Unit Tests for Team Workload and Sprint Capacity Forecaster.
"""

import pytest
from apps.insights.services.workload_forecasting_engine import WorkloadForecastingEngine


class TestWorkloadForecastingEngine:
    def test_optimal_capacity_sprint(self):
        members = [
            {'name': 'Dev 1', 'leave_days': 0, 'assigned_hours': 65.0},
            {'name': 'Dev 2', 'leave_days': 1, 'assigned_hours': 60.0},
            {'name': 'Dev 3', 'leave_days': 0, 'assigned_hours': 68.0},
        ]
        res = WorkloadForecastingEngine.forecast_sprint_capacity('Backend Core', members)
        assert res.total_engineers == 3
        assert res.workload_status in ['OPTIMAL', 'UNDERUTILIZED']
        assert res.estimated_sprint_story_points > 0

    def test_overloaded_sprint_alert(self):
        members = [
            {'name': 'Lead Dev', 'leave_days': 0, 'assigned_hours': 105.0}, # Overloaded
            {'name': 'Senior Dev', 'leave_days': 2, 'assigned_hours': 90.0},
        ]
        res = WorkloadForecastingEngine.forecast_sprint_capacity('Mobile Team', members)
        assert res.workload_status == 'OVERLOADED'
        assert len(res.overload_risk_members) > 0
