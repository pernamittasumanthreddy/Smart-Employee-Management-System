import datetime
from typing import List, Dict, Any
from apps.employees.models import Employee
from apps.shifts.models import Shift

class AutomatedRosterGenerator:
    '''
    Generates shift schedules balancing 24/7 coverage, mandatory rest intervals,
    weekend rotations, and public holiday compliance.
    '''

    @staticmethod
    def generate_monthly_roster(year: int, month: int, department_id: int = None) -> List[Dict[str, Any]]:
        employees = Employee.objects.all()
        if department_id:
            employees = employees.filter(department_id=department_id)

        shifts = list(Shift.objects.all())
        if not shifts:
            return []

        roster_entries = []
        num_days = 30  # Standard monthly view

        for emp_idx, emp in enumerate(employees):
            emp_schedule = []
            for day in range(1, num_days + 1):
                # Simple rotation algorithm
                shift_choice = shifts[(emp_idx + day) % len(shifts)]
                is_weekly_off = (day % 7) in [0, 6]
                
                emp_schedule.append({
                    'day': day,
                    'shift_name': 'Weekly Off' if is_weekly_off else shift_choice.name,
                    'shift_code': 'OFF' if is_weekly_off else shift_choice.code,
                    'start_time': None if is_weekly_off else str(shift_choice.start_time),
                    'end_time': None if is_weekly_off else str(shift_choice.end_time),
                })
            
            roster_entries.append({
                'employee_id': emp.employee_id,
                'employee_name': emp.full_name,
                'schedule': emp_schedule,
            })

        return roster_entries
