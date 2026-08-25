"""
Unit Tests for Indian Income Tax Calculation Engine (Section 115BAC & Old Regime).
"""

from decimal import Decimal
import pytest
from apps.payroll.services.tax_calculator import (
    IncomeTaxCalculationEngine,
    TaxExemptionDeclaration,
    TaxComputationResult
)


class TestIncomeTaxCalculationEngine:
    def test_new_regime_zero_tax_under_7_lakhs(self):
        """Income up to 7,00,000 should have zero tax after standard deduction and 87A rebate."""
        res = IncomeTaxCalculationEngine.calculate_new_regime_tax(Decimal('750000.00'))
        # 7.5L - 75K Std Ded = 6.75L Taxable Income <= 7.0L -> Tax should be 0
        assert res.taxable_income == Decimal('675000.00')
        assert res.total_tax_liability == Decimal('0.00')
        assert res.rebate_87a > Decimal('0.00')

    def test_new_regime_tax_15_lakhs(self):
        """Income of 15,00,000 in New Regime."""
        res = IncomeTaxCalculationEngine.calculate_new_regime_tax(Decimal('1575000.00'))
        # 15.75L - 75K Std Ded = 15.0L Taxable Income
        assert res.taxable_income == Decimal('1500000.00')
        # Slabs: 0-3L (0), 3-7L (20k), 7-10L (30k), 10-12L (30k), 12-15L (60k) = 140,000 + 4% cess = 145,600
        assert res.slab_tax == Decimal('140000.00')
        assert res.total_tax_liability == Decimal('145600.00')

    def test_old_regime_hra_exemption_metro(self):
        """HRA exemption for metro city."""
        basic = Decimal('600000.00')
        hra = Decimal('300000.00')
        rent = Decimal('240000.00')
        exempt = IncomeTaxCalculationEngine.calculate_hra_exemption(basic, hra, rent, is_metro=True)
        # Condition 1: 300,000
        # Condition 2: 50% of 600,000 = 300,000
        # Condition 3: 240,000 - 10% of 600,000 (60,000) = 180,000
        assert exempt == Decimal('180000.00')

    def test_old_regime_chapter_via_capping(self):
        """80C capped at 1.5 Lakhs, 80CCD at 50k, 24b at 2 Lakhs."""
        dec = TaxExemptionDeclaration(
            section_80c=Decimal('250000.00'), # Should cap at 1.5L
            section_80d_self=Decimal('35000.00'), # Cap at 25k
            section_80ccd_1b=Decimal('80000.00'), # Cap at 50k
            section_24b=Decimal('300000.00') # Cap at 2L
        )
        total_ded = IncomeTaxCalculationEngine.calculate_chapter_via_deductions(dec)
        assert total_ded == Decimal('425000.00') # 150k + 25k + 50k + 200k

    def test_regime_comparison(self):
        dec = TaxExemptionDeclaration(section_80c=Decimal('150000.00'), section_80d_self=Decimal('25000.00'))
        comp = IncomeTaxCalculationEngine.compare_regimes(
            gross_income=Decimal('1200000.00'),
            basic_salary=Decimal('500000.00'),
            hra_received=Decimal('250000.00'),
            declaration=dec
        )
        assert comp['recommended_regime'] in ['NEW', 'OLD']
        assert comp['tax_savings'] >= Decimal('0.00')
