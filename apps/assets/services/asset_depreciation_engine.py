"""
Corporate Asset Depreciation & Capital Asset Lifecycle Engine:
Implements Straight Line Method (SLM) and Written Down Value (WDV)
depreciation schedules compliant with Companies Act 2013 (Schedule II).
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional


@dataclass
class AssetDepreciationSchedule:
    asset_id: str
    asset_name: str
    asset_category: str # LAPTOP, SERVER, DESKTOP, FURNITURE, VEHICLE
    original_purchase_cost: Decimal
    useful_life_years: int
    salvage_value_percent: Decimal
    salvage_value: Decimal
    depreciable_base: Decimal
    annual_depreciation_slm: Decimal
    monthly_depreciation_slm: Decimal
    depreciation_schedule_years: List[Dict[str, Decimal]]


class AssetDepreciationEngine:
    """
    Asset lifecycle cost calculation according to Indian Accounting Standards (Ind AS 16).
    """

    USEFUL_LIFE_SCHEDULE = {
        'LAPTOP': 3,
        'SERVER': 6,
        'DESKTOP': 3,
        'FURNITURE': 10,
        'OFFICE_EQUIPMENT': 5,
        'VEHICLE': 8
    }

    @classmethod
    def calculate_slm_depreciation_schedule(
        cls,
        asset_id: str,
        name: str,
        category: str,
        purchase_cost: Decimal,
        salvage_rate_pct: Decimal = Decimal('5.0')
    ) -> AssetDepreciationSchedule:
        cat_key = category.upper()
        useful_life = cls.USEFUL_LIFE_SCHEDULE.get(cat_key, 3)

        salvage_val = (purchase_cost * (salvage_rate_pct / Decimal('100'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        depreciable_base = purchase_cost - salvage_val

        annual_dep = (depreciable_base / Decimal(str(useful_life))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        monthly_dep = (annual_dep / Decimal('12')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        schedule = []
        book_value = purchase_cost

        for year in range(1, useful_life + 1):
            opening_val = book_value
            dep_charge = annual_dep if year < useful_life else (opening_val - salvage_val)
            closing_val = max(salvage_val, opening_val - dep_charge)
            book_value = closing_val

            schedule.append({
                'year': year,
                'opening_book_value': opening_val,
                'depreciation_charge': dep_charge,
                'closing_book_value': closing_val
            })

        return AssetDepreciationSchedule(
            asset_id=asset_id,
            asset_name=name,
            asset_category=category,
            original_purchase_cost=purchase_cost,
            useful_life_years=useful_life,
            salvage_value_percent=salvage_rate_pct,
            salvage_value=salvage_val,
            depreciable_base=depreciable_base,
            annual_depreciation_slm=annual_dep,
            monthly_depreciation_slm=monthly_dep,
            depreciation_schedule_years=schedule
        )
