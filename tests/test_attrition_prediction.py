"""
Unit Tests for ML Attrition Predictor and Retention Risk Scorer.
"""

from decimal import Decimal
import pytest
from apps.insights.services.ml_attrition_predictor import EmployeeAttritionPredictor


class TestEmployeeAttritionPredictor:
    def test_high_risk_employee_detection(self):
        res = EmployeeAttritionPredictor.calculate_flight_risk(
            emp_id='EMP-1001',
            name='Rohit V',
            dept='Engineering',
            current_salary=Decimal('50000.00'),
            benchmark_market_salary=Decimal('90000.00'), # 45% below market
            tenure_months=38,
            months_since_last_promotion=38,
            monthly_avg_overtime_hours=42.0,
            manager_changed_past_6_months=True,
            unplanned_leave_spike_percent=60.0,
            recent_sentiment_score=-0.7
        )
        assert res.flight_risk_score >= 70.0
        assert res.risk_level in ['CRITICAL', 'HIGH']
        assert len(res.key_risk_drivers) >= 3
        assert len(res.retention_recommendations) >= 2

    def test_low_risk_satisfied_employee(self):
        res = EmployeeAttritionPredictor.calculate_flight_risk(
            emp_id='EMP-1002',
            name='Priya S',
            dept='Design',
            current_salary=Decimal('95000.00'),
            benchmark_market_salary=Decimal('90000.00'),
            tenure_months=14,
            months_since_last_promotion=6,
            monthly_avg_overtime_hours=5.0,
            manager_changed_past_6_months=False,
            unplanned_leave_spike_percent=0.0,
            recent_sentiment_score=0.8
        )
        assert res.flight_risk_score <= 30.0
        assert res.risk_level == 'LOW'
