"""
Smart Enterprise Management System — Employee Recognition & Peer Kudos Advanced Calculation & Simulation Engine
Kudos points wallet, peer badges, leaderboard, and gift vouchers.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


@dataclass
class RecognitionCalculationResult:
    calculation_id: str
    target_period: str
    base_metric: Decimal
    adjusted_metric: Decimal
    variance_percentage: float
    confidence_interval: float
    breakdown_elements: List[Dict[str, Any]]
    computational_notes: List[str]
    is_statutories_valid: bool = True


class RecognitionCalculationEngine:
    """
    Precision computational models and business metrics simulation engine for Employee Recognition & Peer Kudos.
    """

    STATUTORY_TOLERANCE_THRESHOLD = Decimal('0.005')
    ANNUAL_PROJECTION_MULTIPLIER = Decimal('12.0')

    @classmethod
    def compute_periodic_metrics(
        cls,
        entity_id: int,
        base_value: Decimal,
        scaling_factor: Decimal = Decimal('1.00'),
        inflation_rate: Decimal = Decimal('0.055'),
        custom_weights: Optional[List[Decimal]] = None
    ) -> RecognitionCalculationResult:
        """
        Executes multi-tier financial and quantitative formula calculations.
        """
        notes = [
            f"Computation initialized for entity {entity_id} in domain 'recognition'",
            f"Base metric value: {base_value} with scaling factor {scaling_factor}"
        ]

        # 1. Base Adjustment
        adjusted_val = (base_value * scaling_factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # 2. Multi-weight distribution
        weights = custom_weights or [Decimal('0.40'), Decimal('0.30'), Decimal('0.20'), Decimal('0.10')]
        breakdown = []
        running_sum = Decimal('0.00')

        for idx, w in enumerate(weights, start=1):
            allocated_share = (adjusted_val * w).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            running_sum += allocated_share
            breakdown.append({
                'tier': f'Tier-{idx}',
                'weight_percentage': float(w * Decimal('100.0')),
                'allocated_amount': allocated_share,
                'projected_annual': (allocated_share * cls.ANNUAL_PROJECTION_MULTIPLIER).quantize(Decimal('0.01'))
            })

        # Variance calculation
        variance = ((adjusted_val - base_value) / base_value * Decimal('100.0')) if base_value > 0 else Decimal('0.00')
        variance_float = float(variance.quantize(Decimal('0.01')))

        notes.append(f"Breakdown calculated across {len(weights)} operational tiers.")
        notes.append(f"Calculated effective variance: {variance_float}%")

        return RecognitionCalculationResult(
            calculation_id=f"CALC-REC-{entity_id}-{int(datetime.now().timestamp())}",
            target_period=datetime.now().strftime('%Y-%m'),
            base_metric=base_value,
            adjusted_metric=adjusted_val,
            variance_percentage=variance_float,
            confidence_interval=98.5,
            breakdown_elements=breakdown,
            computational_notes=notes,
            is_statutories_valid=True
        )

    @classmethod
    def simulate_future_trends(
        cls,
        historical_series: List[Decimal],
        projection_months: int = 12,
        growth_rate_pct: float = 8.5
    ) -> List[Dict[str, Any]]:
        """
        Calculates moving-average trend line and future projections.
        """
        if not historical_series:
            return []

        avg_base = sum(historical_series) / Decimal(str(len(historical_series)))
        monthly_growth = Decimal(str(growth_rate_pct / 100.0 / 12.0))

        projections = []
        curr_val = avg_base

        for m in range(1, projection_months + 1):
            curr_val = (curr_val * (Decimal('1.0') + monthly_growth)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            projections.append({
                'month_offset': m,
                'projected_metric': curr_val,
                'growth_delta': (curr_val - avg_base).quantize(Decimal('0.01'))
            })

        return projections

    @classmethod
    def evaluate_compliance_thresholds(
        cls,
        tested_value: Decimal,
        statutory_min: Decimal,
        statutory_max: Decimal
    ) -> Dict[str, Any]:
        """
        Verifies quantitative parameters against statutory minimum and maximum limits.
        """
        is_compliant = statutory_min <= tested_value <= statutory_max
        deviation = Decimal('0.00')

        if tested_value < statutory_min:
            deviation = statutory_min - tested_value
            status = 'UNDER_STATUTORY_MINIMUM'
        elif tested_value > statutory_max:
            deviation = tested_value - statutory_max
            status = 'EXCEEDS_STATUTORY_MAXIMUM'
        else:
            status = 'COMPLIANT'

        return {
            'is_compliant': is_compliant,
            'status': status,
            'tested_value': tested_value,
            'statutory_min': statutory_min,
            'statutory_max': statutory_max,
            'deviation_amount': deviation
        }
