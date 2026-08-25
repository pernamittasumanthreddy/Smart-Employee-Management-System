"""
Unit Tests for eNPS Statistical Engine.
"""

import pytest
from apps.surveys.services.enps_statistical_engine import ENPSSurveyEngine


class TestENPSSurveyEngine:
    def test_enps_calculation(self):
        # 10 respondents: 6 Promoters (9-10), 2 Passives (7-8), 2 Detractors (0-6)
        ratings = [10, 10, 9, 9, 9, 10, 8, 7, 5, 4]
        res = ENPSSurveyEngine.calculate_enps(ratings)
        assert res.promoters_count == 6
        assert res.passives_count == 2
        assert res.detractors_count == 2
        assert res.promoter_percentage == 60.0
        assert res.detractor_percentage == 20.0
        assert res.enps_score == 40.0 # 60 - 20
        assert res.satisfaction_benchmark == 'GOOD'
