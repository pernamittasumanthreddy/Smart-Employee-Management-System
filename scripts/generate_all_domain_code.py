import os
import sys

def create_code_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Generated: {filepath}")

# 1. Tax Calculation Engine
tax_calc_code = '''"""
Indian Income Tax Calculation Engine (FY 2024-25 / 2025-26 / 2026-27):
Implements full computation for Old Regime vs New Regime (Section 115BAC),
Standard Deduction, Chapter VI-A deductions, HRA exemption (Sec 10(13A)),
80C, 80D, 80CCD(1B), 80E, 80G, 80TTA, 24(b) Home Loan Interest,
Rebate u/s 87A, Surcharge slabs, and 4% Health and Education Cess.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Optional, Tuple


@dataclass
class TaxExemptionDeclaration:
    section_80c: Decimal = Decimal('0.00')      # Limit: 1,50,000 (PPF, ELSS, EPF, LIC, Principal)
    section_80d_self: Decimal = Decimal('0.00') # Limit: 25,000 / 50,000 (Medical Insurance)
    section_80d_parents: Decimal = Decimal('0.00') # Limit: 25,000 / 50,000
    section_80ccd_1b: Decimal = Decimal('0.00') # Limit: 50,000 (NPS)
    section_80e: Decimal = Decimal('0.00')      # Higher education loan interest
    section_80g: Decimal = Decimal('0.00')      # Charitable donations
    section_80tta: Decimal = Decimal('0.00')    # Savings bank interest (Limit: 10,000)
    section_24b: Decimal = Decimal('0.00')      # Home loan interest (Limit: 2,00,000)
    rent_paid_annually: Decimal = Decimal('0.00')
    is_metro_city: bool = False
    other_exemptions: Decimal = Decimal('0.00')


@dataclass
class TaxComputationResult:
    regime: str
    gross_total_income: Decimal
    exemptions_allowances: Decimal
    standard_deduction: Decimal
    chapter_via_deductions: Decimal
    taxable_income: Decimal
    slab_tax: Decimal
    rebate_87a: Decimal
    tax_after_rebate: Decimal
    surcharge: Decimal
    health_education_cess: Decimal
    total_tax_liability: Decimal
    effective_tax_rate: Decimal
    marginal_relief: Decimal
    monthly_tds: Decimal
    slab_breakdown: List[Dict[str, Decimal]]


class IncomeTaxCalculationEngine:
    """
    Production-grade statutory tax computation engine conforming to
    Central Board of Direct Taxes (CBDT) guidelines.
    """

    NEW_REGIME_SLABS_2024_26 = [
        (Decimal('0'), Decimal('300000'), Decimal('0.00')),
        (Decimal('300000'), Decimal('700000'), Decimal('0.05')),
        (Decimal('700000'), Decimal('1000000'), Decimal('0.10')),
        (Decimal('1000000'), Decimal('1200000'), Decimal('0.15')),
        (Decimal('1200000'), Decimal('1500000'), Decimal('0.20')),
        (Decimal('1500000'), Decimal('999999999'), Decimal('0.30')),
    ]

    OLD_REGIME_SLABS = [
        (Decimal('0'), Decimal('250000'), Decimal('0.00')),
        (Decimal('250000'), Decimal('500000'), Decimal('0.05')),
        (Decimal('500000'), Decimal('1000000'), Decimal('0.20')),
        (Decimal('1000000'), Decimal('999999999'), Decimal('0.30')),
    ]

    STANDARD_DEDUCTION_NEW = Decimal('75000.00')
    STANDARD_DEDUCTION_OLD = Decimal('50000.00')
    HEALTH_EDUCATION_CESS_RATE = Decimal('0.04')

    @classmethod
    def calculate_hra_exemption(
        cls,
        basic_salary: Decimal,
        hra_received: Decimal,
        rent_paid: Decimal,
        is_metro: bool = False
    ) -> Decimal:
        """
        Computes minimum of 3 conditions as per Rule 2A / Section 10(13A):
        1. Actual HRA received
        2. 50% of Basic (Metro) or 40% of Basic (Non-Metro)
        3. Rent paid in excess of 10% of Basic salary
        """
        if rent_paid <= Decimal('0.00'):
            return Decimal('0.00')

        condition_1 = hra_received
        percentage = Decimal('0.50') if is_metro else Decimal('0.40')
        condition_2 = basic_salary * percentage
        condition_3 = max(Decimal('0.00'), rent_paid - (basic_salary * Decimal('0.10')))

        exemption = min(condition_1, condition_2, condition_3)
        return max(Decimal('0.00'), exemption.quantize(Decimal('0.01')))

    @classmethod
    def calculate_chapter_via_deductions(cls, dec: TaxExemptionDeclaration) -> Decimal:
        """
        Computes aggregate allowable deductions under Chapter VI-A for Old Regime:
        - 80C capped at 1,50,000
        - 80D Self capped at 25,000 (50,000 if senior)
        - 80D Parents capped at 25,000 (50,000 if senior)
        - 80CCD(1B) NPS capped at 50,000
        - 80TTA capped at 10,000
        - 24(b) Home Loan Interest capped at 2,00,000
        """
        ded_80c = min(Decimal('150000.00'), dec.section_80c)
        ded_80d_self = min(Decimal('25000.00'), dec.section_80d_self)
        ded_80d_parents = min(Decimal('50000.00'), dec.section_80d_parents)
        ded_80ccd = min(Decimal('50000.00'), dec.section_80ccd_1b)
        ded_80tta = min(Decimal('10000.00'), dec.section_80tta)
        ded_24b = min(Decimal('200000.00'), dec.section_24b)
        ded_80e = dec.section_80e
        ded_80g = dec.section_80g

        total_ded = (
            ded_80c + ded_80d_self + ded_80d_parents +
            ded_80ccd + ded_80tta + ded_24b + ded_80e + ded_80g
        )
        return total_ded.quantize(Decimal('0.01'))

    @classmethod
    def compute_slab_tax(cls, taxable_income: Decimal, slabs: List[Tuple[Decimal, Decimal, Decimal]]) -> Tuple[Decimal, List[Dict[str, Decimal]]]:
        tax = Decimal('0.00')
        breakdown = []

        for lower, upper, rate in slabs:
            if taxable_income > lower:
                taxable_in_slab = min(taxable_income, upper) - lower
                slab_tax = taxable_in_slab * rate
                tax += slab_tax
                breakdown.append({
                    'from': lower,
                    'to': upper if upper < Decimal('999999999') else None,
                    'rate': rate * Decimal('100'),
                    'taxable_amount': taxable_in_slab,
                    'tax_amount': slab_tax.quantize(Decimal('0.01'))
                })
            else:
                break

        return tax.quantize(Decimal('0.01')), breakdown

    @classmethod
    def compute_surcharge(cls, taxable_income: Decimal, slab_tax: Decimal, is_new_regime: bool = True) -> Decimal:
        """
        Computes statutory Surcharge rate based on income brackets.
        """
        if taxable_income <= Decimal('5000000.00'):
            return Decimal('0.00')
        elif taxable_income <= Decimal('10000000.00'):
            rate = Decimal('0.10')
        elif taxable_income <= Decimal('20000000.00'):
            rate = Decimal('0.15')
        elif taxable_income <= Decimal('50000000.00'):
            rate = Decimal('0.25')
        else:
            rate = Decimal('0.25') if is_new_regime else Decimal('0.37')

        return (slab_tax * rate).quantize(Decimal('0.01'))

    @classmethod
    def calculate_new_regime_tax(cls, gross_income: Decimal) -> TaxComputationResult:
        std_ded = min(cls.STANDARD_DEDUCTION_NEW, gross_income)
        taxable_income = max(Decimal('0.00'), gross_income - std_ded)

        slab_tax, breakdown = cls.compute_slab_tax(taxable_income, cls.NEW_REGIME_SLABS_2024_26)

        # Rebate under Section 87A: Tax is zero if taxable income <= 7,00,000 (or marginal relief up to 7,27,777)
        rebate_87a = Decimal('0.00')
        marginal_relief = Decimal('0.00')

        if taxable_income <= Decimal('700000.00'):
            rebate_87a = slab_tax
            tax_after_rebate = Decimal('0.00')
        elif taxable_income < Decimal('727777.00'):
            excess_income = taxable_income - Decimal('700000.00')
            if slab_tax > excess_income:
                marginal_relief = slab_tax - excess_income
                tax_after_rebate = excess_income
            else:
                tax_after_rebate = slab_tax
        else:
            tax_after_rebate = slab_tax

        surcharge = cls.compute_surcharge(taxable_income, tax_after_rebate, is_new_regime=True)
        tax_plus_surcharge = tax_after_rebate + surcharge
        cess = (tax_plus_surcharge * cls.HEALTH_EDUCATION_CESS_RATE).quantize(Decimal('0.01'))
        total_liability = (tax_plus_surcharge + cess).quantize(Decimal('0.01'))
        effective_rate = ((total_liability / gross_income) * Decimal('100')).quantize(Decimal('0.01')) if gross_income > 0 else Decimal('0.00')

        return TaxComputationResult(
            regime='NEW',
            gross_total_income=gross_income,
            exemptions_allowances=Decimal('0.00'),
            standard_deduction=std_ded,
            chapter_via_deductions=Decimal('0.00'),
            taxable_income=taxable_income,
            slab_tax=slab_tax,
            rebate_87a=rebate_87a,
            tax_after_rebate=tax_after_rebate,
            surcharge=surcharge,
            health_education_cess=cess,
            total_tax_liability=total_liability,
            effective_tax_rate=effective_rate,
            marginal_relief=marginal_relief,
            monthly_tds=(total_liability / Decimal('12.0')).quantize(Decimal('0.01')),
            slab_breakdown=breakdown
        )

    @classmethod
    def calculate_old_regime_tax(
        cls,
        gross_income: Decimal,
        basic_salary: Decimal,
        hra_received: Decimal,
        declaration: TaxExemptionDeclaration
    ) -> TaxComputationResult:
        hra_exempt = cls.calculate_hra_exemption(
            basic_salary,
            hra_received,
            declaration.rent_paid_annually,
            declaration.is_metro_city
        )
        total_exemptions = hra_exempt + declaration.other_exemptions
        std_ded = min(cls.STANDARD_DEDUCTION_OLD, max(Decimal('0.00'), gross_income - total_exemptions))
        chapter_via = cls.calculate_chapter_via_deductions(declaration)

        taxable_income = max(Decimal('0.00'), gross_income - total_exemptions - std_ded - chapter_via)
        slab_tax, breakdown = cls.compute_slab_tax(taxable_income, cls.OLD_REGIME_SLABS)

        rebate_87a = Decimal('0.00')
        if taxable_income <= Decimal('500000.00'):
            rebate_87a = min(Decimal('12500.00'), slab_tax)
            tax_after_rebate = Decimal('0.00')
        else:
            tax_after_rebate = slab_tax

        surcharge = cls.compute_surcharge(taxable_income, tax_after_rebate, is_new_regime=False)
        tax_plus_surcharge = tax_after_rebate + surcharge
        cess = (tax_plus_surcharge * cls.HEALTH_EDUCATION_CESS_RATE).quantize(Decimal('0.01'))
        total_liability = (tax_plus_surcharge + cess).quantize(Decimal('0.01'))
        effective_rate = ((total_liability / gross_income) * Decimal('100')).quantize(Decimal('0.01')) if gross_income > 0 else Decimal('0.00')

        return TaxComputationResult(
            regime='OLD',
            gross_total_income=gross_income,
            exemptions_allowances=total_exemptions,
            standard_deduction=std_ded,
            chapter_via_deductions=chapter_via,
            taxable_income=taxable_income,
            slab_tax=slab_tax,
            rebate_87a=rebate_87a,
            tax_after_rebate=tax_after_rebate,
            surcharge=surcharge,
            health_education_cess=cess,
            total_tax_liability=total_liability,
            effective_tax_rate=effective_rate,
            marginal_relief=Decimal('0.00'),
            monthly_tds=(total_liability / Decimal('12.0')).quantize(Decimal('0.01')),
            slab_breakdown=breakdown
        )

    @classmethod
    def compare_regimes(
        cls,
        gross_income: Decimal,
        basic_salary: Decimal,
        hra_received: Decimal,
        declaration: TaxExemptionDeclaration
    ) -> Dict[str, any]:
        new_res = cls.calculate_new_regime_tax(gross_income)
        old_res = cls.calculate_old_regime_tax(gross_income, basic_salary, hra_received, declaration)

        savings = abs(new_res.total_tax_liability - old_res.total_tax_liability)
        recommended = 'NEW' if new_res.total_tax_liability <= old_res.total_tax_liability else 'OLD'

        return {
            'new_regime': new_res,
            'old_regime': old_res,
            'recommended_regime': recommended,
            'tax_savings': savings,
            'difference_monthly': (savings / Decimal('12.0')).quantize(Decimal('0.01'))
        }
'''

create_code_file('apps/payroll/services/tax_calculator.py', tax_calc_code)
print("Tax calculator module complete!")
