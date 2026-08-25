"""
Unit Tests for Asset Depreciation Schedule Calculator (SLM Method).
"""

from decimal import Decimal
import pytest
from apps.assets.services.asset_depreciation_engine import AssetDepreciationEngine


class TestAssetDepreciationEngine:
    def test_laptop_depreciation_3_years(self):
        res = AssetDepreciationEngine.calculate_slm_depreciation_schedule(
            asset_id='AST-LAP-001',
            name='MacBook Pro 16',
            category='LAPTOP',
            purchase_cost=Decimal('200000.00'),
            salvage_rate_pct=Decimal('5.0') # Salvage = 10,000, Depreciable = 190,000
        )
        assert res.useful_life_years == 3
        assert res.salvage_value == Decimal('10000.00')
        assert res.depreciable_base == Decimal('190000.00')
        assert len(res.depreciation_schedule_years) == 3
        assert res.depreciation_schedule_years[-1]['closing_book_value'] == Decimal('10000.00')
