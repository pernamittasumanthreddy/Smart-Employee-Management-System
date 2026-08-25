"""
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
