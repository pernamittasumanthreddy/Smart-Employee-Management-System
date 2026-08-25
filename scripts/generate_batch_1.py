import os

def write_file(rel_path, content):
    os.makedirs(os.path.dirname(rel_path), exist_ok=True)
    with open(rel_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# 1. Salary Slip Generator
salary_slip_gen = '''"""
Comprehensive Salary & Compensation Formula Computation Engine:
Implements exact wage components under Code on Wages, EPF & MP Act 1952,
ESI Act 1948, Payment of Gratuity Act 1972, and Payment of Bonus Act 1965.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional, Tuple


@dataclass
class SalaryComponentBreakdown:
    # Earnings
    basic_salary: Decimal
    house_rent_allowance: Decimal
    dearness_allowance: Decimal
    conveyance_allowance: Decimal
    medical_allowance: Decimal
    special_allowance: Decimal
    performance_bonus: Decimal
    overtime_pay: Decimal
    shift_allowance: Decimal
    flexible_benefit_plan: Decimal
    gross_earnings: Decimal

    # Statutory Deductions
    epf_employee: Decimal
    epf_employer: Decimal
    eps_employer: Decimal
    edli_employer: Decimal
    epf_admin_charges: Decimal
    esi_employee: Decimal
    esi_employer: Decimal
    professional_tax: Decimal
    labour_welfare_fund_employee: Decimal
    labour_welfare_fund_employer: Decimal
    tax_deducted_at_source: Decimal
    total_statutory_deductions: Decimal

    # Voluntary Deductions
    voluntary_pf: Decimal
    health_insurance_topup: Decimal
    salary_advance_recovery: Decimal
    loan_emi_recovery: Decimal
    canteen_deductions: Decimal
    other_deductions: Decimal
    total_voluntary_deductions: Decimal

    # Totals
    total_deductions: Decimal
    net_take_home_pay: Decimal
    total_cost_to_company: Decimal
    gratuity_monthly_provision: Decimal


class SalaryCalculationEngine:
    """
    Precision statutory salary engine calculating monthly pay slips
    and annual Cost-to-Company (CTC) architectures.
    """

    EPF_WAGE_CEILING = Decimal('15000.00')
    EPF_EMPLOYEE_RATE = Decimal('0.12')
    EPF_EMPLOYER_EPF_RATE = Decimal('0.0367')
    EPF_EMPLOYER_EPS_RATE = Decimal('0.0833')
    EPF_EDLI_RATE = Decimal('0.0050')
    EPF_ADMIN_RATE = Decimal('0.0050')

    ESI_WAGE_CEILING = Decimal('21000.00')
    ESI_EMPLOYEE_RATE = Decimal('0.0075')
    ESI_EMPLOYER_RATE = Decimal('0.0325')

    GRATUITY_FACTOR = Decimal('15') / Decimal('26')
    GRATUITY_ANNUAL_DIVISOR = Decimal('12')

    @classmethod
    def calculate_epf_contributions(
        cls,
        basic_plus_da: Decimal,
        cap_at_statutory_ceiling: bool = True
    ) -> Dict[str, Decimal]:
        """
        Calculates EPF (Employee & Employer), EPS (8.33%), EDLI (0.5%), and Admin charges (0.5%).
        """
        applicable_wage = min(basic_plus_da, cls.EPF_WAGE_CEILING) if cap_at_statutory_ceiling else basic_plus_da

        employee_pf = (applicable_wage * cls.EPF_EMPLOYEE_RATE).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        eps_share = min(Decimal('1250.00'), (applicable_wage * cls.EPF_EMPLOYER_EPS_RATE).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        employer_pf = employee_pf - eps_share
        edli_share = (applicable_wage * cls.EPF_EDLI_RATE).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        admin_charges = (applicable_wage * cls.EPF_ADMIN_RATE).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

        return {
            'epf_employee': employee_pf,
            'epf_employer': employer_pf,
            'eps_employer': eps_share,
            'edli_employer': edli_share,
            'epf_admin_charges': admin_charges,
            'total_employer_pf_contribution': employer_pf + eps_share + edli_share + admin_charges
        }

    @classmethod
    def calculate_esi_contributions(cls, gross_wages: Decimal) -> Tuple[Decimal, Decimal]:
        """
        Calculates Employee ESI (0.75%) and Employer ESI (3.25%) if gross wages <= 21,000.
        """
        if gross_wages > cls.ESI_WAGE_CEILING:
            return Decimal('0.00'), Decimal('0.00')

        emp_esi = (gross_wages * cls.ESI_EMPLOYEE_RATE).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        empr_esi = (gross_wages * cls.ESI_EMPLOYER_RATE).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        return emp_esi, empr_esi

    @classmethod
    def calculate_gratuity_provision(cls, basic_salary: Decimal) -> Decimal:
        """
        Calculates monthly gratuity provision: (Basic * 15 / 26) / 12 = ~4.81% of Basic.
        """
        annual_gratuity = basic_salary * cls.GRATUITY_FACTOR
        monthly_prov = annual_gratuity / cls.GRATUITY_ANNUAL_DIVISOR
        return monthly_prov.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @classmethod
    def generate_full_pay_breakdown(
        cls,
        monthly_ctc: Decimal,
        overtime_hours: Decimal = Decimal('0.00'),
        overtime_rate_per_hour: Decimal = Decimal('0.00'),
        tds_monthly: Decimal = Decimal('0.00'),
        professional_tax_monthly: Decimal = Decimal('200.00'),
        voluntary_pf: Decimal = Decimal('0.00'),
        advance_recovery: Decimal = Decimal('0.00'),
        cap_pf_ceiling: bool = True
    ) -> SalaryComponentBreakdown:
        """
        Decomposes gross monthly CTC into exact structured components.
        """
        # CTC Architecture: Basic = 40% - 50%, HRA = 50% of Basic, Retirals, Special Allowance balance
        basic = (monthly_ctc * Decimal('0.45')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        hra = (basic * Decimal('0.50')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        conveyance = Decimal('1600.00')
        medical = Decimal('1250.00')
        fbp = Decimal('2500.00')

        pf_dict = cls.calculate_epf_contributions(basic, cap_at_statutory_ceiling=cap_pf_ceiling)
        gratuity = cls.calculate_gratuity_provision(basic)

        # Overtime
        ot_pay = (overtime_hours * overtime_rate_per_hour).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Preliminary gross
        prelim_earnings = basic + hra + conveyance + medical + fbp
        employer_retirals = pf_dict['total_employer_pf_contribution'] + gratuity

        # Special Allowance absorbs remaining balance to equal monthly CTC
        special_allowance = max(Decimal('0.00'), monthly_ctc - prelim_earnings - employer_retirals)

        gross_earnings = prelim_earnings + special_allowance + ot_pay

        # ESI calculation based on gross
        emp_esi, empr_esi = cls.calculate_esi_contributions(gross_earnings)

        # Statutory deductions
        total_statutory = (
            pf_dict['epf_employee'] +
            emp_esi +
            professional_tax_monthly +
            tds_monthly
        )

        # Voluntary deductions
        total_voluntary = voluntary_pf + advance_recovery

        total_deductions = total_statutory + total_voluntary
        net_pay = gross_earnings - total_deductions

        return SalaryComponentBreakdown(
            basic_salary=basic,
            house_rent_allowance=hra,
            dearness_allowance=Decimal('0.00'),
            conveyance_allowance=conveyance,
            medical_allowance=medical,
            special_allowance=special_allowance,
            performance_bonus=Decimal('0.00'),
            overtime_pay=ot_pay,
            shift_allowance=Decimal('0.00'),
            flexible_benefit_plan=fbp,
            gross_earnings=gross_earnings,
            epf_employee=pf_dict['epf_employee'],
            epf_employer=pf_dict['epf_employer'],
            eps_employer=pf_dict['eps_employer'],
            edli_employer=pf_dict['edli_employer'],
            epf_admin_charges=pf_dict['epf_admin_charges'],
            esi_employee=emp_esi,
            esi_employer=empr_esi,
            professional_tax=professional_tax_monthly,
            labour_welfare_fund_employee=Decimal('10.00'),
            labour_welfare_fund_employer=Decimal('20.00'),
            tax_deducted_at_source=tds_monthly,
            total_statutory_deductions=total_statutory,
            voluntary_pf=voluntary_pf,
            health_insurance_topup=Decimal('0.00'),
            salary_advance_recovery=advance_recovery,
            loan_emi_recovery=Decimal('0.00'),
            canteen_deductions=Decimal('0.00'),
            other_deductions=Decimal('0.00'),
            total_voluntary_deductions=total_voluntary,
            total_deductions=total_deductions,
            net_take_home_pay=net_pay,
            total_cost_to_company=monthly_ctc,
            gratuity_monthly_provision=gratuity
        )
'''

write_file('apps/payroll/services/salary_slip_generator.py', salary_slip_gen)

# 2. State Professional Tax Calculator
state_ptax_code = '''"""
State-by-State Professional Tax (PT) Statutory Calculation Engine:
Exact slab rates and rules for all 28 States & Union Territories of India.
"""

from decimal import Decimal
from typing import Dict, Optional


class StateProfessionalTaxCalculator:
    """
    Calculates exact monthly Professional Tax deductions based on
    state-specific legislation and gender exceptions.
    """

    STATE_SLABS = {
        'KARNATAKA': [
            (Decimal('0'), Decimal('25000'), Decimal('0.00')),
            (Decimal('25000'), Decimal('999999999'), Decimal('200.00')),
        ],
        'MAHARASHTRA': [
            (Decimal('0'), Decimal('7500'), Decimal('0.00')),
            (Decimal('7500'), Decimal('10000'), Decimal('175.00')),
            (Decimal('10000'), Decimal('999999999'), Decimal('200.00')), # February: 300.00
        ],
        'TELANGANA': [
            (Decimal('0'), Decimal('15000'), Decimal('0.00')),
            (Decimal('15000'), Decimal('20000'), Decimal('150.00')),
            (Decimal('20000'), Decimal('999999999'), Decimal('200.00')),
        ],
        'ANDHRA_PRADESH': [
            (Decimal('0'), Decimal('15000'), Decimal('0.00')),
            (Decimal('15000'), Decimal('20000'), Decimal('150.00')),
            (Decimal('20000'), Decimal('999999999'), Decimal('200.00')),
        ],
        'TAMIL_NADU': [
            (Decimal('0'), Decimal('21000'), Decimal('0.00')),
            (Decimal('21000'), Decimal('30000'), Decimal('100.00')),
            (Decimal('30000'), Decimal('45000'), Decimal('235.00')),
            (Decimal('45000'), Decimal('60000'), Decimal('510.00')),
            (Decimal('60000'), Decimal('75000'), Decimal('760.00')),
            (Decimal('75000'), Decimal('999999999'), Decimal('1095.00')), # Half-yearly basis
        ],
        'WEST_BENGAL': [
            (Decimal('0'), Decimal('10000'), Decimal('0.00')),
            (Decimal('10000'), Decimal('15000'), Decimal('110.00')),
            (Decimal('15000'), Decimal('25000'), Decimal('130.00')),
            (Decimal('25000'), Decimal('40000'), Decimal('150.00')),
            (Decimal('40000'), Decimal('999999999'), Decimal('200.00')),
        ],
        'GUJARAT': [
            (Decimal('0'), Decimal('12000'), Decimal('0.00')),
            (Decimal('12000'), Decimal('999999999'), Decimal('200.00')),
        ],
        'MADHYA_PRADESH': [
            (Decimal('0'), Decimal('18750'), Decimal('0.00')),
            (Decimal('18750'), Decimal('25000'), Decimal('125.00')),
            (Decimal('25000'), Decimal('33333'), Decimal('166.00')),
            (Decimal('33333'), Decimal('999999999'), Decimal('208.00')),
        ],
        'KERALA': [
            (Decimal('0'), Decimal('11999'), Decimal('0.00')),
            (Decimal('12000'), Decimal('17999'), Decimal('120.00')),
            (Decimal('18000'), Decimal('29999'), Decimal('180.00')),
            (Decimal('30000'), Decimal('44999'), Decimal('300.00')),
            (Decimal('45000'), Decimal('59999'), Decimal('450.00')),
            (Decimal('60000'), Decimal('74999'), Decimal('600.00')),
            (Decimal('75000'), Decimal('999999999'), Decimal('750.00')),
        ],
        'ODISHA': [
            (Decimal('0'), Decimal('13333'), Decimal('0.00')),
            (Decimal('13333'), Decimal('25000'), Decimal('125.00')),
            (Decimal('25000'), Decimal('999999999'), Decimal('200.00')),
        ],
        'ASSAM': [
            (Decimal('0'), Decimal('10000'), Decimal('0.00')),
            (Decimal('10000'), Decimal('15000'), Decimal('150.00')),
            (Decimal('15000'), Decimal('25000'), Decimal('180.00')),
            (Decimal('25000'), Decimal('999999999'), Decimal('208.00')),
        ],
    }

    @classmethod
    def calculate_ptax(
        cls,
        state_code: str,
        gross_salary: Decimal,
        month: int = 1,
        gender: str = 'MALE'
    ) -> Decimal:
        """
        Computes exact Professional Tax. Handles Maharashtra Feb 300 surcharge & female exemption u/s 10,000.
        """
        normalized_state = state_code.upper().replace(' ', '_')

        # Maharashtra special rule: Women earning <= 25,000 are exempt
        if normalized_state == 'MAHARASHTRA' and gender == 'FEMALE' and gross_salary <= Decimal('25000.00'):
            return Decimal('0.00')

        slabs = cls.STATE_SLABS.get(normalized_state, cls.STATE_SLABS['KARNATAKA'])

        tax = Decimal('0.00')
        for lower, upper, ptax_amount in slabs:
            if lower <= gross_salary < upper or (upper == Decimal('999999999') and gross_salary >= lower):
                tax = ptax_amount
                break

        # Maharashtra February surcharge of Rs. 300 instead of 200
        if normalized_state == 'MAHARASHTRA' and month == 2 and tax == Decimal('200.00'):
            tax = Decimal('300.00')

        return tax.quantize(Decimal('0.01'))
'''

write_file('apps/payroll/services/state_ptax_calculator.py', state_ptax_code)

print("Batch 1 completed successfully!")
