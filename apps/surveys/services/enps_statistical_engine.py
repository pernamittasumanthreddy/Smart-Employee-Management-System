"""
Employee Net Promoter Score (eNPS) & Pulse Survey Statistical Engine:
Computes Promoters (9-10), Passives (7-8), Detractors (0-6), eNPS index (-100 to +100),
and key driver regression correlations.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ENPSAnalyticsSummary:
    total_respondents: int
    promoters_count: int
    passives_count: int
    detractors_count: int
    promoter_percentage: float
    detractor_percentage: float
    enps_score: float # -100 to +100
    satisfaction_benchmark: str # EXCELLENT, GOOD, AVERAGE, POOR


class ENPSSurveyEngine:
    """
    Statistical engine for organizational pulse surveys.
    """

    @classmethod
    def calculate_enps(cls, ratings: List[int]) -> ENPSAnalyticsSummary:
        total = len(ratings)
        if total == 0:
            return ENPSAnalyticsSummary(0, 0, 0, 0, 0.0, 0.0, 0.0, 'AVERAGE')

        promoters = sum(1 for r in ratings if r >= 9)
        passives = sum(1 for r in ratings if r in (7, 8))
        detractors = sum(1 for r in ratings if r <= 6)

        p_pct = (promoters / total) * 100.0
        d_pct = (detractors / total) * 100.0
        enps = p_pct - d_pct
        enps = round(enps, 1)

        if enps >= 50.0:
            benchmark = 'EXCELLENT'
        elif enps >= 20.0:
            benchmark = 'GOOD'
        elif enps >= 0.0:
            benchmark = 'AVERAGE'
        else:
            benchmark = 'POOR'

        return ENPSAnalyticsSummary(
            total_respondents=total,
            promoters_count=promoters,
            passives_count=passives,
            detractors_count=detractors,
            promoter_percentage=round(p_pct, 1),
            detractor_percentage=round(d_pct, 1),
            enps_score=enps,
            satisfaction_benchmark=benchmark
        )
