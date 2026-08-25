"""
Interview Scorecard & Panel Evaluation Aggregator:
Aggregates technical, system design, coding, cultural, and leadership scores.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ConsolidatedInterviewEvaluation:
    candidate_id: int
    candidate_name: str
    total_rounds_conducted: int
    overall_weighted_score: float # 1.0 to 5.0
    hire_recommendation: str      # STRONG_HIRE, HIRE, LEAN_HIRE, REJECT, STRONG_REJECT
    round_scores: List[Dict]
    consensus_strengths: List[str]
    consensus_concerns: List[str]


class InterviewScorecardAggregator:
    """
    Weighted interview score aggregator and hiring consensus computer.
    """

    ROUND_WEIGHTS = {
        'TECHNICAL_ROUND_1': 0.30,
        'SYSTEM_DESIGN_ROUND': 0.30,
        'CODING_LIVE': 0.20,
        'CULTURE_FIT': 0.10,
        'MANAGERIAL_HR': 0.10,
    }

    @classmethod
    def compute_evaluation(
        cls,
        cand_id: int,
        name: str,
        evaluations: List[Dict]
    ) -> ConsolidatedInterviewEvaluation:
        weighted_sum = 0.0
        total_weight = 0.0
        strengths = []
        concerns = []
        breakdown = []

        for e in evaluations:
            r_type = e.get('round_type', 'TECHNICAL_ROUND_1')
            weight = cls.ROUND_WEIGHTS.get(r_type, 0.20)
            score = float(e.get('score', 3.0)) # Scale 1 to 5

            weighted_sum += score * weight
            total_weight += weight

            if e.get('strength'):
                strengths.append(f"[{r_type}] {e.get('strength')}")
            if e.get('concern'):
                concerns.append(f"[{r_type}] {e.get('concern')}")

            breakdown.append({
                'interviewer': e.get('interviewer_name', 'Senior Panelist'),
                'round': r_type,
                'score': score,
                'weight': weight
            })

        overall_score = (weighted_sum / total_weight) if total_weight > 0 else 3.0
        overall_score = round(overall_score, 2)

        if overall_score >= 4.5:
            rec = 'STRONG_HIRE'
        elif overall_score >= 3.8:
            rec = 'HIRE'
        elif overall_score >= 3.0:
            rec = 'LEAN_HIRE'
        elif overall_score >= 2.0:
            rec = 'REJECT'
        else:
            rec = 'STRONG_REJECT'

        return ConsolidatedInterviewEvaluation(
            candidate_id=cand_id,
            candidate_name=name,
            total_rounds_conducted=len(evaluations),
            overall_weighted_score=overall_score,
            hire_recommendation=rec,
            round_scores=breakdown,
            consensus_strengths=strengths,
            consensus_concerns=concerns
        )
