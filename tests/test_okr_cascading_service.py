"""
Unit Tests for OKR Cascading Progress Engine.
"""

import pytest
from apps.goals.services.okr_cascading_engine import OKRCascadingEngine


class TestOKRCascadingEngine:
    def test_okr_weighted_progress(self):
        krs = [
            {'title': 'Deliver Microservices', 'current_value': 80, 'target_value': 100, 'weight': 2.0}, # 80% * 2 = 160
            {'title': 'Achieve 99.9% Uptime', 'current_value': 100, 'target_value': 100, 'weight': 1.0}, # 100% * 1 = 100
        ]
        res = OKRCascadingEngine.calculate_objective_progress(1, 'Cloud Modernization', 'DevOps', krs)
        # Total weight = 3.0, weighted sum = 260 -> 260 / 3 = 86.7%
        assert res.overall_progress_percent == 86.7
        assert res.health_status == 'ON_TRACK'
