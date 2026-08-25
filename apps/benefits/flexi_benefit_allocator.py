from decimal import Decimal
from typing import Dict, Any

class FlexibleBenefitPlanAllocator:
    '''
    Optimizes Indian Tax Savings via Flexible Benefit Plan (FBP) components:
    - Fuel & Driver Allowance (Rule 3)
    - Food / Meal Coupons (₹2,200/mo exempt)
    - Telephone & Broadband Reimbursement (100% on actuals)
    - Books & Periodicals Allowance
    - National Pension Scheme (NPS) corporate deduction
    '''

    @staticmethod
    def calculate_optimal_fbp_distribution(annual_special_allowance: Decimal) -> Dict[str, Any]:
        # Maximum statutory allocation allocations
        meal_coupons_annual = Decimal('26400.00')  # 2200 * 12
        broadband_annual = Decimal('24000.00')     # 2000 * 12
        fuel_conveyance_annual = Decimal('39600.00') # 3300 * 12
        learning_books_annual = Decimal('12000.00') # 1000 * 12

        total_fbp = meal_coupons_annual + broadband_annual + fuel_conveyance_annual + learning_books_annual
        applicable_fbp = min(total_fbp, annual_special_allowance)
        annual_tax_saved = (applicable_fbp * Decimal('0.30')).quantize(Decimal('0.01'))  # 30% tax bracket

        return {
            'total_fbp_allocated': applicable_fbp,
            'meal_coupons': meal_coupons_annual,
            'broadband_allowance': broadband_annual,
            'fuel_allowance': fuel_conveyance_annual,
            'learning_allowance': learning_books_annual,
            'estimated_annual_tax_saved_inr': annual_tax_saved,
        }
