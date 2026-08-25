"""
Smart Employee Management System — AI Analytics ML Advanced KPI & Metrics Calculator
Attrition score updates, anomaly detections, and trend alerts.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional


@dataclass
class PerformanceKPISnapshot:
    module_name: str
    total_volume_processed: int
    success_rate_percent: float
    total_financial_impact: Decimal
    period_start: date
    period_end: date
    trend_indicator: str # UPWARD, STABLE, DOWNWARD


class InsightsMetricsCalculator:
    """
    Real-time KPI metrics and financial impact aggregator for AI Analytics ML.
    """

    @classmethod
    def calculate_period_kpis(
        cls,
        records: List[Dict[str, Any]],
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> PerformanceKPISnapshot:
        s_date = start_date or date.today().replace(day=1)
        e_date = end_date or date.today()

        total = len(records)
        if total == 0:
            return PerformanceKPISnapshot(
                module_name="insights",
                total_volume_processed=0,
                success_rate_percent=100.0,
                total_financial_impact=Decimal('0.00'),
                period_start=s_date,
                period_end=e_date,
                trend_indicator='STABLE'
            )

        success_count = sum(1 for r in records if r.get('is_success', True))
        rate = (success_count / total * 100.0) if total > 0 else 100.0
        fin_impact = sum(Decimal(str(r.get('amount', 0.0))) for r in records)

        trend = 'UPWARD' if rate >= 90.0 else ('DOWNWARD' if rate < 75.0 else 'STABLE')

        return PerformanceKPISnapshot(
            module_name="insights",
            total_volume_processed=total,
            success_rate_percent=round(rate, 1),
            total_financial_impact=fin_impact.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            period_start=s_date,
            period_end=e_date,
            trend_indicator=trend
        )
