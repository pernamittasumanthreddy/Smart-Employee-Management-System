"""
Performance 9-Box Grid & Bell Curve Normalization Engine:
Maps Performance Rating vs Potential Rating, calculates merit increase matrices,
and performs forced-ranking Gaussian distribution fit.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Tuple


@dataclass
class NineBoxPlacement:
    employee_id: int
    employee_name: str
    performance_score: float # 1.0 to 5.0
    potential_score: float   # 1.0 to 5.0
    box_code: str            # STAR, HIGH_POTENTIAL, CORE_PLAYER, RISK, etc.
    box_label: str
    talent_action_plan: str
    recommended_increment_percent: Decimal


class AppraisalMatrixEngine:
    """
    9-Box Grid and compensation merit matrix calculator.
    """

    NINE_BOX_DEFINITIONS = {
        'HIGH_PERF_HIGH_POT': ('STAR', 'Future Leader / Star Talent', 'Fast-track promotion, retention grant, executive mentoring.', Decimal('18.0')),
        'HIGH_PERF_MED_POT': ('HIGH_PRO', 'High Professional / Core Driver', 'Expand technical scope, peer mentorship, bonus recognition.', Decimal('14.0')),
        'HIGH_PERF_LOW_POT': ('SOLID_PRO', 'Solid Professional / Key Contributor', 'Keep challenged in current role, specialized mastery.', Decimal('10.0')),
        'MED_PERF_HIGH_POT': ('EMERGING_LEADER', 'Emerging Talent / Growth Driver', 'Provide stretch assignments, targeted skill training.', Decimal('12.0')),
        'MED_PERF_MED_POT': ('CORE_PLAYER', 'Core Player / Effective Performer', 'Standard progression, performance calibration.', Decimal('9.0')),
        'MED_PERF_LOW_POT': ('EFFECTIVE', 'Effective Specialist', 'Review goal alignment and process efficiency.', Decimal('6.0')),
        'LOW_PERF_HIGH_POT': ('ENIGMA', 'Enigma / High Potential Underperformer', 'Investigate root cause, pair with mentor, role realignment.', Decimal('5.0')),
        'LOW_PERF_MED_POT': ('DILEMMA', 'Dilemma / Inconsistent Contributor', 'Initiate 60-day coaching plan, clarify KPI targets.', Decimal('3.0')),
        'LOW_PERF_LOW_POT': ('UNDERPERFORMER', 'Talent Risk / Underperformer', 'Initiate formal Performance Improvement Plan (PIP) or transition.', Decimal('0.0')),
    }

    @classmethod
    def evaluate_9_box(cls, emp_id: int, name: str, perf_score: float, pot_score: float) -> NineBoxPlacement:
        # Determine performance tier
        if perf_score >= 4.0:
            p_tier = 'HIGH_PERF'
        elif perf_score >= 3.0:
            p_tier = 'MED_PERF'
        else:
            p_tier = 'LOW_PERF'

        # Determine potential tier
        if pot_score >= 4.0:
            pot_tier = 'HIGH_POT'
        elif pot_score >= 3.0:
            pot_tier = 'MED_POT'
        else:
            pot_tier = 'LOW_POT'

        key = f"{p_tier}_{pot_tier}"
        box_code, label, action, increment = cls.NINE_BOX_DEFINITIONS.get(key, cls.NINE_BOX_DEFINITIONS['MED_PERF_MED_POT'])

        return NineBoxPlacement(
            employee_id=emp_id,
            employee_name=name,
            performance_score=perf_score,
            potential_score=pot_score,
            box_code=box_code,
            box_label=label,
            talent_action_plan=action,
            recommended_increment_percent=increment
        )
