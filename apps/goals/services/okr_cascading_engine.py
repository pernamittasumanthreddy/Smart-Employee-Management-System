"""
Strategic OKR (Objectives & Key Results) Cascading & Alignment Engine:
Computes hierarchical goal rollups, weighted KR progress, and confidence indices.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class OKRProgressRollup:
    objective_id: int
    objective_title: str
    overall_progress_percent: float
    health_status: str # ON_TRACK, AT_RISK, BEHIND
    total_key_results: int
    aligned_department: str
    key_results_summary: List[Dict]


class OKRCascadingEngine:
    """
    Calculates weighted progress rollups for OKRs across the company.
    """

    @classmethod
    def calculate_objective_progress(
        cls,
        obj_id: int,
        title: str,
        dept: str,
        key_results: List[Dict]
    ) -> OKRProgressRollup:
        total_krs = len(key_results)
        if total_krs == 0:
            return OKRProgressRollup(obj_id, title, 0.0, 'AT_RISK', 0, dept, [])

        total_weighted_progress = 0.0
        total_weight = 0.0
        summaries = []

        for kr in key_results:
            current = float(kr.get('current_value', 0.0))
            target = float(kr.get('target_value', 100.0))
            weight = float(kr.get('weight', 1.0))

            kr_pct = (current / target * 100.0) if target > 0 else 0.0
            kr_pct = min(100.0, max(0.0, kr_pct))

            total_weighted_progress += kr_pct * weight
            total_weight += weight

            summaries.append({
                'title': kr.get('title', 'Key Result'),
                'progress_pct': round(kr_pct, 1),
                'current': current,
                'target': target
            })

        overall_pct = (total_weighted_progress / total_weight) if total_weight > 0 else 0.0
        overall_pct = round(overall_pct, 1)

        if overall_pct >= 70.0:
            status = 'ON_TRACK'
        elif overall_pct >= 40.0:
            status = 'AT_RISK'
        else:
            status = 'BEHIND'

        return OKRProgressRollup(
            objective_id=obj_id,
            objective_title=title,
            overall_progress_percent=overall_pct,
            health_status=status,
            total_key_results=total_krs,
            aligned_department=dept,
            key_results_summary=summaries
        )
