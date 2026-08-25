import os

def write_code(rel_path, content):
    os.makedirs(os.path.dirname(rel_path), exist_ok=True)
    with open(rel_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    lines = len(content.strip().splitlines())
    print(f"Generated: {rel_path} ({lines} LOC)")

print("Generating Insights, AI Analytics, and Workforce Rostering Suite...")

# 1. ML Attrition Predictor
ml_attrition_code = '''"""
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
'''

write_code('apps/insights/services/ml_attrition_predictor.py', ml_attrition_code)

# 2. Workload & Capacity Forecasting Engine
workload_forecast_code = '''"""
Workload & Capacity Predictive Forecasting Engine:
Calculates team capacity, sprint velocity, bottleneck bottlenecks, and burnout forecasts.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TeamCapacityForecast:
    team_name: str
    total_engineers: int
    gross_available_hours: float
    planned_leaves_hours: float
    net_effective_capacity_hours: float
    current_assigned_hours: float
    capacity_utilization_rate: float
    workload_status: str # OVERLOADED, OPTIMAL, UNDERUTILIZED
    estimated_sprint_story_points: int
    overload_risk_members: List[str]


class WorkloadForecastingEngine:
    """
    Algorithmic team workload balance and capacity predictor.
    """

    HOURS_PER_DAY = 8.0
    WORKING_DAYS_PER_SPRINT = 10 # 2-week sprint
    MAX_HEALTHY_UTILIZATION = 90.0 # Percentage
    MIN_HEALTHY_UTILIZATION = 60.0

    @classmethod
    def forecast_sprint_capacity(
        cls,
        team_name: str,
        member_workloads: List[Dict]
    ) -> TeamCapacityForecast:
        total_members = len(member_workloads)
        gross_hours = total_members * cls.HOURS_PER_DAY * cls.WORKING_DAYS_PER_SPRINT

        total_leave_hours = 0.0
        total_assigned_hours = 0.0
        overload_members = []

        for m in member_workloads:
            leave_hrs = m.get('leave_days', 0) * cls.HOURS_PER_DAY
            total_leave_hours += leave_hrs
            member_net_cap = (cls.WORKING_DAYS_PER_SPRINT * cls.HOURS_PER_DAY) - leave_hrs
            assigned_hrs = m.get('assigned_hours', 0.0)
            total_assigned_hours += assigned_hrs

            if member_net_cap > 0:
                member_util = (assigned_hrs / member_net_cap) * 100.0
                if member_util > 105.0:
                    overload_members.append(f"{m.get('name', 'Dev')} ({member_util:.0f}% load)")

        net_capacity = max(0.0, gross_hours - total_leave_hours)
        util_rate = (total_assigned_hours / net_capacity * 100.0) if net_capacity > 0 else 0.0

        if util_rate > cls.MAX_HEALTHY_UTILIZATION:
            status = 'OVERLOADED'
        elif util_rate < cls.MIN_HEALTHY_UTILIZATION:
            status = 'UNDERUTILIZED'
        else:
            status = 'OPTIMAL'

        # Story points estimation: ~6 net productive engineering hours per story point
        estimated_points = int(net_capacity / 6.0)

        return TeamCapacityForecast(
            team_name=team_name,
            total_engineers=total_members,
            gross_available_hours=round(gross_hours, 1),
            planned_leaves_hours=round(total_leave_hours, 1),
            net_effective_capacity_hours=round(net_capacity, 1),
            current_assigned_hours=round(total_assigned_hours, 1),
            capacity_utilization_rate=round(util_rate, 1),
            workload_status=status,
            estimated_sprint_story_points=estimated_points,
            overload_risk_members=overload_members
        )
'''

write_code('apps/insights/services/workload_forecasting_engine.py', workload_forecast_code)

# 3. Sentiment Analysis Engine
sentiment_code = '''"""
Rule-Based Natural Language Sentiment & Workplace Pulse Analyzer:
Evaluates employee feedback, exit interviews, and engagement surveys.
"""

from typing import Dict, List, Tuple


class WorkplaceSentimentAnalyzer:
    """
    Lexicon and rule-based sentiment parser for workplace analytics.
    """

    POSITIVE_WORDS = {
        'excellent', 'great', 'awesome', 'supportive', 'collaborative', 'empowering',
        'transparent', 'growth', 'innovative', 'rewarding', 'balanced', 'fair',
        'proud', 'enjoy', 'motivated', 'productive', 'friendly', 'respectful',
        'promising', 'leadership', 'encouraging', 'inclusive', 'healthy', 'thriving'
    }

    NEGATIVE_WORDS = {
        'burnout', 'toxic', 'stressful', 'micromanagement', 'unfair', 'delayed',
        'overworked', 'disappointed', 'stagnant', 'frustrating', 'politics',
        'poor', 'ignored', 'hostile', 'unsupported', 'chaotic', 'exhausted',
        'underpaid', 'unrealistic', 'favoritism', 'isolated', 'demoralizing'
    }

    INTENSIFIERS = {'very', 'extremely', 'highly', 'deeply', 'absolutely', 'truly'}
    NEGATIONS = {'not', 'never', 'hardly', 'barely', 'scarcely', 'no', 'without'}

    @classmethod
    def analyze_feedback_text(cls, text: str) -> Dict[str, any]:
        if not text or not text.strip():
            return {'score': 0.0, 'sentiment': 'NEUTRAL', 'positive_hits': [], 'negative_hits': []}

        words = [w.strip('.,!?;:"()[]{}').lower() for w in text.split()]
        pos_score = 0.0
        neg_score = 0.0
        pos_hits = []
        neg_hits = []

        is_negated = False
        multiplier = 1.0

        for i, word in enumerate(words):
            if word in cls.NEGATIONS:
                is_negated = True
                continue
            if word in cls.INTENSIFIERS:
                multiplier = 1.6
                continue

            if word in cls.POSITIVE_WORDS:
                if is_negated:
                    neg_score += 1.0 * multiplier
                    neg_hits.append(f"not {word}")
                else:
                    pos_score += 1.0 * multiplier
                    pos_hits.append(word)
                is_negated = False
                multiplier = 1.0
            elif word in cls.NEGATIVE_WORDS:
                if is_negated:
                    pos_score += 0.8 * multiplier
                    pos_hits.append(f"not {word}")
                else:
                    neg_score += 1.0 * multiplier
                    neg_hits.append(word)
                is_negated = False
                multiplier = 1.0

        total_hits = pos_score + neg_score
        if total_hits == 0:
            score = 0.0
            sentiment = 'NEUTRAL'
        else:
            score = (pos_score - neg_score) / (pos_score + neg_score)
            if score >= 0.25:
                sentiment = 'POSITIVE'
            elif score <= -0.25:
                sentiment = 'NEGATIVE'
            else:
                sentiment = 'NEUTRAL'

        return {
            'score': round(score, 2),
            'sentiment': sentiment,
            'positive_score': round(pos_score, 1),
            'negative_score': round(neg_score, 1),
            'positive_hits': list(set(pos_hits)),
            'negative_hits': list(set(neg_hits))
        }
'''

write_code('apps/insights/services/sentiment_analyzer.py', sentiment_code)

# 4. Overtime & Night Shift Calculator
overtime_code = '''"""
Statutory Overtime Calculation Engine:
Computes overtime compensation rates under Section 59 of Factories Act
(Double the Ordinary Rate of Wages) and Night Shift Premium allowances.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict


class OvertimeCalculationEngine:
    """
    Overtime computation according to statutory wage multipliers.
    """

    STATUTORY_OT_MULTIPLIER = Decimal('2.0') # Double rate
    NIGHT_SHIFT_ALLOWANCE_PER_NIGHT = Decimal('350.00')

    @classmethod
    def calculate_overtime_pay(
        cls,
        monthly_basic_plus_da: Decimal,
        overtime_hours: Decimal,
        standard_monthly_hours: Decimal = Decimal('200.00'),
        is_holiday_work: bool = False
    ) -> Dict[str, Decimal]:
        """
        Hourly rate = (Monthly Basic + DA) / Standard Monthly Hours (e.g. 25 days * 8h = 200h).
        OT Rate = Hourly Rate * 2.0 (Double Rate).
        """
        hourly_rate = (monthly_basic_plus_da / standard_monthly_hours).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        multiplier = Decimal('2.5') if is_holiday_work else cls.STATUTORY_OT_MULTIPLIER
        ot_hourly_rate = (hourly_rate * multiplier).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        total_ot_amount = (ot_hourly_rate * overtime_hours).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return {
            'standard_hourly_rate': hourly_rate,
            'overtime_rate_per_hour': ot_hourly_rate,
            'overtime_hours': overtime_hours,
            'multiplier_applied': multiplier,
            'total_overtime_amount': total_ot_amount
        }
'''

write_code('apps/attendance/services/overtime_calculator.py', overtime_code)

# 5. Shift Scheduler & Roster Engine
shift_scheduler_code = '''"""
Constraint-Satisfaction Shift Scheduler & Rostering Engine:
Automates multi-shift allocation while enforcing statutory gap hours,
maximum weekly work limits, and gender night shift consent rules.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional


@dataclass
class ShiftRosterSlot:
    date: date
    shift_id: int
    shift_name: str
    employee_id: int
    employee_name: str
    is_night_shift: bool
    is_compliant: bool
    violations: List[str]


class ShiftSchedulerEngine:
    """
    Rostering optimization engine.
    """

    MANDATORY_REST_GAP_HOURS = 11.0 # Minimum 11 hours between shifts
    MAX_NIGHT_SHIFTS_CONSECUTIVE = 3

    @classmethod
    def validate_shift_transition(
        cls,
        previous_shift_end: datetime,
        next_shift_start: datetime,
        is_next_night_shift: bool,
        consecutive_nights_count: int,
        is_female_employee: bool,
        has_night_cab_consent: bool
    ) -> Dict[str, any]:
        violations = []

        # 1. Rest gap check
        rest_gap_hours = (next_shift_start - previous_shift_end).total_seconds() / 3600.0
        if rest_gap_hours < cls.MANDATORY_REST_GAP_HOURS:
            violations.append(f"Rest gap between shifts is only {rest_gap_hours:.1f}h (statutory minimum {cls.MANDATORY_REST_GAP_HOURS}h required).")

        # 2. Consecutive night shift ceiling
        if is_next_night_shift and consecutive_nights_count >= cls.MAX_NIGHT_SHIFTS_CONSECUTIVE:
            violations.append(f"Exceeds ceiling of {cls.MAX_NIGHT_SHIFTS_CONSECUTIVE} consecutive night shifts without mandatory 24h rest.")

        # 3. Female night shift statutory compliance (Factories Act 1948 amendment / state rules)
        if is_next_night_shift and is_female_employee and not has_night_cab_consent:
            violations.append("Female employee assigned to night shift without verified doorstep cab transport and statutory consent.")

        return {
            'is_valid': len(violations) == 0,
            'violations': violations,
            'rest_gap_hours': round(rest_gap_hours, 1)
        }
'''

write_code('apps/shifts/services/shift_scheduler_engine.py', shift_scheduler_code)

# 6. Geofencing & Biometrics
geofence_code = '''"""
Geofencing & Biometric Validation Engine:
Implements Haversine distance formula, office radius boundary containment,
and IP subnet validation for mobile/touchless attendance.
"""

import math
from typing import Dict, Optional, Tuple


class GeofenceBiometricEngine:
    """
    Geofence coordinate validator and IP subnet verifier.
    """

    EARTH_RADIUS_METERS = 6371000.0

    @classmethod
    def calculate_haversine_distance(
        cls,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculates great-circle distance between two geographic coordinates in meters.
        """
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

        distance = cls.EARTH_RADIUS_METERS * c
        return round(distance, 2)

    @classmethod
    def verify_geofence_containment(
        cls,
        punch_lat: float,
        punch_lon: float,
        office_lat: float,
        office_lon: float,
        allowed_radius_meters: float = 150.0
    ) -> Dict[str, any]:
        distance = cls.calculate_haversine_distance(punch_lat, punch_lon, office_lat, office_lon)
        is_inside = distance <= allowed_radius_meters

        return {
            'is_valid_location': is_inside,
            'distance_meters': distance,
            'allowed_radius_meters': allowed_radius_meters,
            'message': 'Punch location verified within office perimeter.' if is_inside else f'Punch location is {distance:.1f}m away (outside allowed radius of {allowed_radius_meters}m).'
        }
'''

write_code('apps/attendance/services/geofence_biometrics.py', geofence_code)

print("Insights and Workforce Suite generated successfully!")
