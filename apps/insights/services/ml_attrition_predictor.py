"""
Employee Flight Risk & Attrition Predictive Intelligence Engine:
Implements multi-factor heuristic model assessing retention risk factors,
compensation market ratio, manager friction index, and engagement signals.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Optional, Tuple


@dataclass
class AttritionRiskAssessment:
    employee_id: str
    employee_name: str
    department: str
    flight_risk_score: float # 0.0 to 100.0
    risk_level: str          # CRITICAL, HIGH, MEDIUM, LOW
    key_risk_drivers: List[str]
    retention_recommendations: List[str]
    market_salary_ratio: float
    tenure_months: int
    overtime_stress_index: float
    promotion_stagnation_index: float


class EmployeeAttritionPredictor:
    """
    Predictive analytics engine for employee retention management.
    """

    # Weights for Risk Factors
    W_COMPENSATION = 0.28
    W_TENURE_STAGNATION = 0.22
    W_OVERTIME_BURNOUT = 0.18
    W_MANAGER_CHANGE = 0.12
    W_LEAVE_SPIKE = 0.10
    W_ENGAGEMENT_SENTIMENT = 0.10

    @classmethod
    def calculate_flight_risk(
        cls,
        emp_id: str,
        name: str,
        dept: str,
        current_salary: Decimal,
        benchmark_market_salary: Decimal,
        tenure_months: int,
        months_since_last_promotion: int,
        monthly_avg_overtime_hours: float,
        manager_changed_past_6_months: bool,
        unplanned_leave_spike_percent: float,
        recent_sentiment_score: float # -1.0 to +1.0
    ) -> AttritionRiskAssessment:
        risk_drivers = []
        recommendations = []
        raw_risk_score = 0.0

        # 1. Compensation Parity (Comp-ratio)
        market_ratio = float(current_salary / benchmark_market_salary) if benchmark_market_salary > 0 else 1.0
        if market_ratio < 0.75:
            comp_risk = 100.0
            risk_drivers.append(f"Severe compensation gap: earning {(1.0-market_ratio)*100:.1f}% below market benchmark.")
            recommendations.append("Initiate off-cycle compensation correction or equity retention grant.")
        elif market_ratio < 0.90:
            comp_risk = 60.0
            risk_drivers.append(f"Below market median: earning {(1.0-market_ratio)*100:.1f}% below target band.")
            recommendations.append("Align compensation in upcoming annual appraisal cycle.")
        else:
            comp_risk = 10.0

        raw_risk_score += comp_risk * cls.W_COMPENSATION

        # 2. Promotion Stagnation Index
        if months_since_last_promotion > 36:
            stag_risk = 90.0
            risk_drivers.append(f"Promotion stagnation: {months_since_last_promotion} months without title/role progression.")
            recommendations.append("Conduct career development review and establish leadership pathway.")
        elif months_since_last_promotion > 24:
            stag_risk = 55.0
            risk_drivers.append(f"Tenure in current role: {months_since_last_promotion} months without milestone.")
            recommendations.append("Explore horizontal skill rotation or high-impact project assignment.")
        else:
            stag_risk = 15.0

        raw_risk_score += stag_risk * cls.W_TENURE_STAGNATION

        # 3. Overtime Burnout Risk
        if monthly_avg_overtime_hours > 35.0:
            ot_risk = 95.0
            risk_drivers.append(f"Severe burnout risk: averaging {monthly_avg_overtime_hours:.1f} overtime hours/month.")
            recommendations.append("Mandate workload rebalancing and compensatory rest leaves.")
        elif monthly_avg_overtime_hours > 20.0:
            ot_risk = 60.0
            risk_drivers.append(f"Elevated overtime strain: averaging {monthly_avg_overtime_hours:.1f} hours/month.")
            recommendations.append("Review project delivery timeline commitments.")
        else:
            ot_risk = 10.0

        raw_risk_score += ot_risk * cls.W_OVERTIME_BURNOUT

        # 4. Managerial Change Disruption
        mgr_risk = 70.0 if manager_changed_past_6_months else 10.0
        if manager_changed_past_6_months:
            risk_drivers.append("Recent reporting manager transition within last 6 months.")
            recommendations.append("Schedule 1-on-1 check-in with new reporting manager to ensure alignment.")

        raw_risk_score += mgr_risk * cls.W_MANAGER_CHANGE

        # 5. Leave Pattern Disruption
        if unplanned_leave_spike_percent > 50.0:
            leave_risk = 85.0
            risk_drivers.append(f"Sudden leave spike: {unplanned_leave_spike_percent:.1f}% increase in unplanned leaves.")
        elif unplanned_leave_spike_percent > 25.0:
            leave_risk = 50.0
            risk_drivers.append(f"Moderate leave increase: {unplanned_leave_spike_percent:.1f}% above historical baseline.")
        else:
            leave_risk = 10.0

        raw_risk_score += leave_risk * cls.W_LEAVE_SPIKE

        # 6. Sentiment Index (-1.0 to +1.0 converted to 100 to 0 risk)
        normalized_sentiment_risk = (1.0 - recent_sentiment_score) * 50.0
        raw_risk_score += normalized_sentiment_risk * cls.W_ENGAGEMENT_SENTIMENT

        final_score = round(min(100.0, max(0.0, raw_risk_score)), 1)

        if final_score >= 75.0:
            level = 'CRITICAL'
        elif final_score >= 50.0:
            level = 'HIGH'
        elif final_score >= 25.0:
            level = 'MEDIUM'
        else:
            level = 'LOW'

        return AttritionRiskAssessment(
            employee_id=emp_id,
            employee_name=name,
            department=dept,
            flight_risk_score=final_score,
            risk_level=level,
            key_risk_drivers=risk_drivers,
            retention_recommendations=recommendations,
            market_salary_ratio=round(market_ratio, 2),
            tenure_months=tenure_months,
            overtime_stress_index=round(ot_risk, 1),
            promotion_stagnation_index=round(stag_risk, 1)
        )
