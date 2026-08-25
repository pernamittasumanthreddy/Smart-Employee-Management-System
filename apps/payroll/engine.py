from decimal import Decimal
from typing import Dict, Any, List

class IndianIncomeTaxEngine:
    '''
    Comprehensive calculation engine for Indian Income Tax under Chapter XII-BA of Income Tax Act 1961.
    Supports both the New Concessional Tax Regime (Section 115BAC) and the Old Tax Regime with standard deductions,
    Section 80C, Section 80D, Section 24(b) Home Loan Interest, HRA Exemptions under Section 10(13A), and Section 87A rebate.
    '''

    # Tax Slabs for New Regime (FY 2026-27 / AY 2027-28)
    NEW_REGIME_SLABS = [
        (Decimal('0.00'), Decimal('300000.00'), Decimal('0.00')),
        (Decimal('300000.00'), Decimal('700000.00'), Decimal('0.05')),
        (Decimal('700000.00'), Decimal('1000000.00'), Decimal('0.10')),
        (Decimal('1000000.00'), Decimal('1200000.00'), Decimal('0.15')),
        (Decimal('1200000.00'), Decimal('1500000.00'), Decimal('0.20')),
        (Decimal('1500000.00'), Decimal('999999999.00'), Decimal('0.30')),
    ]
    NEW_REGIME_STANDARD_DEDUCTION = Decimal('75000.00')
    NEW_REGIME_REBATE_LIMIT = Decimal('700000.00')

    # Tax Slabs for Old Regime
    OLD_REGIME_SLABS = [
        (Decimal('0.00'), Decimal('250000.00'), Decimal('0.00')),
        (Decimal('250000.00'), Decimal('500000.00'), Decimal('0.05')),
        (Decimal('500000.00'), Decimal('1000000.00'), Decimal('0.20')),
        (Decimal('1000000.00'), Decimal('999999999.00'), Decimal('0.30')),
    ]
    OLD_REGIME_STANDARD_DEDUCTION = Decimal('50000.00')
    OLD_REGIME_REBATE_LIMIT = Decimal('500000.00')

    HEALTH_AND_EDUCATION_CESS_RATE = Decimal('0.04')

    @classmethod
    def calculate_hra_exemption(cls, annual_basic: Decimal, annual_hra_received: Decimal, annual_rent_paid: Decimal, is_metro: bool = True) -> Decimal:
        '''
        Calculates exempt House Rent Allowance under Section 10(13A) rule 2A:
        Minimum of:
        1. Actual HRA received
        2. Rent paid excess of 10% of Basic salary
        3. 50% of Basic salary (if metro city like Bengaluru/Mumbai/Delhi) or 40% (non-metro)
        '''
        if annual_rent_paid <= Decimal('0.00') or annual_hra_received <= Decimal('0.00'):
            return Decimal('0.00')
        
        limit_1 = annual_hra_received
        limit_2 = max(Decimal('0.00'), annual_rent_paid - (annual_basic * Decimal('0.10')))
        limit_3 = annual_basic * (Decimal('0.50') if is_metro else Decimal('0.40'))
        
        return min(limit_1, limit_2, limit_3).quantize(Decimal('0.01'))

    @classmethod
    def compute_old_regime_tax(
        cls,
        gross_annual_salary: Decimal,
        annual_basic: Decimal,
        annual_hra_received: Decimal,
        annual_rent_paid: Decimal,
        sec_80c_total: Decimal = Decimal('0.00'),
        sec_80d_self: Decimal = Decimal('0.00'),
        sec_80d_parents: Decimal = Decimal('0.00'),
        home_loan_interest_sec24: Decimal = Decimal('0.00'),
        nps_sec_80ccd_1b: Decimal = Decimal('0.00'),
        professional_tax_annual: Decimal = Decimal('2400.00'),
    ) -> Dict[str, Any]:
        # 1. Deductions under Section 16
        std_deduction = cls.OLD_REGIME_STANDARD_DEDUCTION
        hra_exemption = cls.calculate_hra_exemption(annual_basic, annual_hra_received, annual_rent_paid)
        
        income_from_salary = gross_annual_salary - std_deduction - professional_tax_annual - hra_exemption
        income_from_salary = max(Decimal('0.00'), income_from_salary)

        # 2. Loss from House Property (Section 24b - capped at 2,00,000)
        home_loan_ded = min(Decimal('200000.00'), home_loan_interest_sec24)
        gross_total_income = max(Decimal('0.00'), income_from_salary - home_loan_ded)

        # 3. Chapter VI-A Deductions
        ded_80c = min(Decimal('150000.00'), sec_80c_total)
        ded_80d_self = min(Decimal('25000.00'), sec_80d_self)
        ded_80d_parents = min(Decimal('50000.00'), sec_80d_parents)
        ded_nps = min(Decimal('50000.00'), nps_sec_80ccd_1b)
        total_chapter_via = ded_80c + ded_80d_self + ded_80d_parents + ded_nps

        net_taxable_income = max(Decimal('0.00'), gross_total_income - total_chapter_via)

        # 4. Tax Slab Computation
        tax_before_cess = Decimal('0.00')
        remaining = net_taxable_income

        for lower, upper, rate in cls.OLD_REGIME_SLABS:
            if remaining > lower:
                taxable_in_slab = min(remaining, upper) - lower
                tax_before_cess += (taxable_in_slab * rate)

        # Rebate under Section 87A
        if net_taxable_income <= cls.OLD_REGIME_REBATE_LIMIT:
            tax_before_cess = Decimal('0.00')

        # Surcharge (if applicable > 50 Lakhs)
        surcharge = Decimal('0.00')
        if net_taxable_income > Decimal('5000000.00'):
            surcharge = tax_before_cess * Decimal('0.10')

        cess = (tax_before_cess + surcharge) * cls.HEALTH_AND_EDUCATION_CESS_RATE
        total_tax = (tax_before_cess + surcharge + cess).quantize(Decimal('0.01'))
        monthly_tds = (total_tax / Decimal('12.0')).quantize(Decimal('0.01'))

        return {
            'regime': 'OLD',
            'gross_annual_salary': gross_annual_salary,
            'standard_deduction': std_deduction,
            'hra_exemption': hra_exemption,
            'chapter_via_deductions': total_chapter_via,
            'net_taxable_income': net_taxable_income,
            'tax_before_cess': tax_before_cess.quantize(Decimal('0.01')),
            'cess': cess.quantize(Decimal('0.01')),
            'total_annual_tax': total_tax,
            'monthly_tds': monthly_tds,
        }

    @classmethod
    def compute_new_regime_tax(cls, gross_annual_salary: Decimal) -> Dict[str, Any]:
        std_deduction = cls.NEW_REGIME_STANDARD_DEDUCTION
        net_taxable_income = max(Decimal('0.00'), gross_annual_salary - std_deduction)

        tax_before_cess = Decimal('0.00')
        for lower, upper, rate in cls.NEW_REGIME_SLABS:
            if net_taxable_income > lower:
                taxable_in_slab = min(net_taxable_income, upper) - lower
                tax_before_cess += (taxable_in_slab * rate)

        # Rebate under Section 87A up to 7 Lakhs
        if net_taxable_income <= cls.NEW_REGIME_REBATE_LIMIT:
            tax_before_cess = Decimal('0.00')

        cess = tax_before_cess * cls.HEALTH_AND_EDUCATION_CESS_RATE
        total_tax = (tax_before_cess + cess).quantize(Decimal('0.01'))
        monthly_tds = (total_tax / Decimal('12.0')).quantize(Decimal('0.01'))

        return {
            'regime': 'NEW',
            'gross_annual_salary': gross_annual_salary,
            'standard_deduction': std_deduction,
            'net_taxable_income': net_taxable_income,
            'tax_before_cess': tax_before_cess.quantize(Decimal('0.01')),
            'cess': cess.quantize(Decimal('0.01')),
            'total_annual_tax': total_tax,
            'monthly_tds': monthly_tds,
        }

    @classmethod
    def generate_regime_comparison(cls, gross_annual_salary: Decimal, basic: Decimal, hra: Decimal, rent: Decimal, deductions_80c: Decimal, ded_80d: Decimal) -> Dict[str, Any]:
        old_res = cls.compute_old_regime_tax(gross_annual_salary, basic, hra, rent, sec_80c_total=deductions_80c, sec_80d_self=ded_80d)
        new_res = cls.compute_new_regime_tax(gross_annual_salary)
        
        diff = old_res['total_annual_tax'] - new_res['total_annual_tax']
        recommended = 'NEW' if diff >= 0 else 'OLD'
        savings = abs(diff)

        return {
            'old_regime': old_res,
            'new_regime': new_res,
            'recommended_regime': recommended,
            'annual_savings': savings,
        }
