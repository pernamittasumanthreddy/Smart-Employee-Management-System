"""
Smart Enterprise Management System — Training Domain Engine
Computes skill proficiency gaps between current role proficiencies and target designations, recommending relevant training modules.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Callable, Dict, List, Optional, Set, Tuple



@dataclass
class SkillGapAnalysisReport:
    employee_id: int
current_designation: str
target_designation: str
overall_competency_readiness_pct: float
skill_gap_breakdown: List[Dict]
recommended_training_courses: List[str]
mandatory_compliance_certifications_pending: List[str]


class SkillGapMatrixEngine:
    """
    Evaluates skill matrices and automates learning curriculum paths.
    """

    @classmethod
    def analyze_skill_gaps(cls, emp_id: int, current_role: str, target_role: str, current_skills: Dict[str, int], required_target_skills: Dict[str, int]) -> SkillGapAnalysisReport:
        """
        Calculates proficiency score deltas and maps gaps to course catalog.
        """
        gap_details = []
total_weight = 0
earned_weight = 0
recommended_courses = []

for skill, target_level in required_target_skills.items():
    current_level = current_skills.get(skill, 0)
    gap = max(0, target_level - current_level)
    total_weight += target_level
    earned_weight += min(current_level, target_level)

    gap_details.append({
        "skill": skill,
        "current_proficiency": current_level,
        "required_proficiency": target_level,
        "proficiency_gap": gap
    })

    if gap > 0:
        recommended_courses.append(f"Mastering {skill.title()} (Level {target_level} Track)")

readiness_pct = (earned_weight / total_weight * 100.0) if total_weight > 0 else 100.0

return SkillGapAnalysisReport(
    employee_id=emp_id,
    current_designation=current_role,
    target_designation=target_role,
    overall_competency_readiness_pct=round(readiness_pct, 1),
    skill_gap_breakdown=gap_details,
    recommended_training_courses=recommended_courses,
    mandatory_compliance_certifications_pending=["POSH Annual Refresher 2026", "Information Security (ISMS 27001)"]
)
