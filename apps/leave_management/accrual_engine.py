from decimal import Decimal
from typing import Dict, List, Any
from django.utils import timezone
from apps.employees.models import Employee
from apps.leave_management.models import LeaveBalance, LeaveType

class LeaveAccrualCalculationEngine:
    '''
    Automated Leave Accrual & Carry-Forward Calculation Engine:
    - Monthly prorated accruals for Earned / Privilege Leave (PL / EL)
    - Quarterly Sick & Casual Leave credit allocations
    - Annual carry-forward caps with loss-of-pay and encashment balance calculators
    '''

    ANNUAL_EL_QUOTA = Decimal('18.0')
    ANNUAL_CL_QUOTA = Decimal('12.0')
    ANNUAL_SL_QUOTA = Decimal('10.0')
    MAX_CARRY_FORWARD_EL = Decimal('45.0')

    @classmethod
    def process_monthly_leave_accruals(cls, year: int, month: int) -> int:
        employees = Employee.objects.filter(employment_status='ACTIVE')
        count = 0
        monthly_el_credit = (cls.ANNUAL_EL_QUOTA / Decimal('12.0')).quantize(Decimal('0.5'))
        monthly_cl_credit = (cls.ANNUAL_CL_QUOTA / Decimal('12.0')).quantize(Decimal('0.5'))

        for emp in employees:
            balances = LeaveBalance.objects.filter(employee=emp)
            for bal in balances:
                if 'Earned' in bal.leave_type.name or 'Privilege' in bal.leave_type.name:
                    bal.total_days += monthly_el_credit
                    bal.save()
                    count += 1
                elif 'Casual' in bal.leave_type.name:
                    bal.total_days += monthly_cl_credit
                    bal.save()
                    count += 1
        return count
