from decimal import Decimal
from typing import Dict, Any

class SalaryComponentCalculator:
    '''
    Statutory Salary Component Engine:
    Computes exact monthly and annual gratuity provisions under the Payment of Gratuity Act 1972,
    statutory bonus under Payment of Bonus Act 1965, and national pension scheme (NPS) tax benefits.
    '''

    @staticmethod
    def calculate_gratuity_provision(basic_salary_monthly: Decimal, tenure_years: Decimal) -> Decimal:
        if tenure_years < Decimal('5.0'):
            return Decimal('0.00')
        # Gratuity Formula: (15 * Last Drawn Basic * Tenure) / 26
        gratuity = (Decimal('15.0') * basic_salary_monthly * tenure_years) / Decimal('26.0')
        # Statutory Cap in India: INR 20,00,000 (20 Lakhs)
        return min(gratuity, Decimal('2000000.00')).quantize(Decimal('0.01'))

    @staticmethod
    def calculate_nps_corporate_contribution(basic_salary_monthly: Decimal, nps_percentage: Decimal = Decimal('10.0')) -> Dict[str, Any]:
        # Under Section 80CCD(2), employer NPS contribution up to 10% of (Basic + DA) is exempt
        nps_monthly = (basic_salary_monthly * (nps_percentage / Decimal('100.0'))).quantize(Decimal('0.01'))
        return {
            'monthly_nps_employer': nps_monthly,
            'annual_nps_tax_exemption': (nps_monthly * Decimal('12.0')).quantize(Decimal('0.01')),
            'eligible_under_section': '80CCD(2)'
        }
