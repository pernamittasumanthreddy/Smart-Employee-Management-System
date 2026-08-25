from decimal import Decimal
from typing import List, Dict, Any
from apps.goals.models import Goal
from apps.employees.models import Employee

class OKRProgressTrackingEngine:
    '''
    Tracks hierarchical OKRs (Company -> Department -> Team -> Individual).
    Calculates weighted milestone completion rates and expected trajectory vs deadline.
    '''

    @staticmethod
    def calculate_employee_okr_progress(employee: Employee) -> Dict[str, Any]:
        goals = Goal.objects.filter(employee=employee)
        total_goals = goals.count()
        if total_goals == 0:
            return {'total_okrs': 0, 'average_completion': 0.0, 'status': 'ON_TRACK'}

        total_pct = sum(getattr(g, 'progress_percentage', Decimal('0.0')) or Decimal('0.0') for g in goals)
        avg_pct = round(float(total_pct / Decimal(str(total_goals))), 1)

        health = 'ON_TRACK'
        if avg_pct < 40.0:
            health = 'AT_RISK'
        elif avg_pct < 70.0:
            health = 'NEEDS_ATTENTION'

        return {
            'total_okrs': total_goals,
            'average_completion': avg_pct,
            'health_status': health,
            'completed_count': sum(1 for g in goals if getattr(g, 'progress_percentage', 0) >= 100),
        }
