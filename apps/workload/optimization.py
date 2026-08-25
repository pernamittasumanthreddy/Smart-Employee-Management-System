from decimal import Decimal
from typing import Dict, List, Any
from apps.employees.models import Employee
from apps.tasks.models import Task
from apps.projects.models import Project

class WorkloadBalancingEngine:
    '''
    Analyzes team capacity, task estimates, sprint deadlines, and overtime patterns
    to detect team member burnout risks and suggest automated load rebalancing.
    '''

    @staticmethod
    def analyze_team_capacity_utilization() -> List[Dict[str, Any]]:
        employees = Employee.objects.select_related('department', 'designation').all()
        results = []

        for emp in employees:
            assigned_tasks = Task.objects.filter(assigned_to=emp, status__in=['TODO', 'IN_PROGRESS', 'REVIEW'])
            total_active_tasks = assigned_tasks.count()
            estimated_hours = sum(getattr(t, 'estimated_hours', Decimal('6.0')) or Decimal('6.0') for t in assigned_tasks)
            
            standard_weekly_capacity = Decimal('40.00')
            load_percentage = ((Decimal(estimated_hours) / standard_weekly_capacity) * Decimal('100.00')).quantize(Decimal('0.1'))
            
            risk_level = 'OPTIMAL'
            if load_percentage > Decimal('125.0'):
                risk_level = 'CRITICAL_OVERLOAD'
            elif load_percentage > Decimal('105.0'):
                risk_level = 'ELEVATED_LOAD'
            elif load_percentage < Decimal('60.0'):
                risk_level = 'UNDERUTILIZED'

            results.append({
                'employee_id': emp.id,
                'name': emp.full_name,
                'department': emp.department.name if emp.department else 'General',
                'active_tasks_count': total_active_tasks,
                'allocated_hours': float(estimated_hours),
                'load_percentage': float(load_percentage),
                'burnout_risk_level': risk_level,
                'rebalance_recommended': risk_level == 'CRITICAL_OVERLOAD',
            })
        return sorted(results, key=lambda x: x['load_percentage'], reverse=True)
