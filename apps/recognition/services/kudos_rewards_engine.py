"""
Smart Enterprise Management System — Recognition Domain Engine
Computes recognition leaderboard rankings, points-to-currency redemption values, and corporate gift voucher catalogs.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


@dataclass
class KudosWalletSummary:
    employee_id: int
    total_kudos_received: int
    total_points_balance: int
    redeemable_cash_equivalent_inr: Decimal
    leaderboard_rank: int
    badges_earned: List[str]
    eligible_voucher_catalog: List[Dict]


class KudosRewardsEngine:
    """
    Recognition points valuation and gift voucher redemption engine.
    """

    @classmethod
    def compute_wallet_and_vouchers(
        cls,
        emp_id: int,
        points_balance: int,
        kudos_count: int,
        all_team_scores: List[int]
    ) -> KudosWalletSummary:
        """
        1 Recognition Point = Rs. 2.00 cash voucher value. Computes leaderboard rank.
        """
        point_to_inr_multiplier = Decimal("2.00")
        cash_value = (Decimal(str(points_balance)) * point_to_inr_multiplier).quantize(Decimal("0.01"))

        sorted_scores = sorted(all_team_scores, reverse=True)
        rank = sorted_scores.index(points_balance) + 1 if points_balance in sorted_scores else len(sorted_scores) + 1

        badges = []
        if kudos_count >= 20:
            badges.append("Corporate Legend")
        elif kudos_count >= 10:
            badges.append("Team Champion")
        elif kudos_count >= 5:
            badges.append("Rising Star")

        vouchers = [
            {"name": "Amazon eGift Card", "points_required": 500, "inr_value": 1000},
            {"name": "Flipkart Digital Voucher", "points_required": 500, "inr_value": 1000},
            {"name": "BookMyShow Movie Pass", "points_required": 250, "inr_value": 500},
            {"name": "Zomato Gourmet Dining", "points_required": 500, "inr_value": 1000}
        ]

        return KudosWalletSummary(
            employee_id=emp_id,
            total_kudos_received=kudos_count,
            total_points_balance=points_balance,
            redeemable_cash_equivalent_inr=cash_value,
            leaderboard_rank=rank,
            badges_earned=badges,
            eligible_voucher_catalog=vouchers
        )
