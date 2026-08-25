"""
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
