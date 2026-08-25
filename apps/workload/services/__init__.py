from decimal import Decimal

from django.utils import timezone

from apps.employees.models import Employee
from apps.workload.models import (
    EmployeeWorkloadMetric,
    UtilizationStatus,
    WorkloadHistory,
)


class WorkloadCalculationService:
    """
    Mathematical and multi-factor workload index computation.
    Evaluates task count, priority weights, estimated hours, deadlines, and overdue tasks.
    """

    PRIORITY_WEIGHTS = {
        'URGENT': 3.0,
        'HIGH': 2.0,
        'MEDIUM': 1.0,
        'LOW': 0.5,
    }

    @classmethod
    def calculate_for_employee(cls, employee):
        # Retrieve active tasks
        tasks = getattr(employee, 'assigned_tasks', None)
        if not tasks:
            score = 0
            active_count = 0
            est_hours = Decimal('0.0')
            overdue_count = 0
            proj_count = 0
        else:
            active_tasks = tasks.filter(status__in=['TODO', 'IN_PROGRESS', 'REVIEW'])
            active_count = active_tasks.count()
            
            today = timezone.now().date()
            overdue_tasks = active_tasks.filter(due_date__lt=today)
            overdue_count = overdue_tasks.count()

            # Sum of weighted hours
            weighted_workload_sum = 0.0
            total_est_hours = 0.0

            for task in active_tasks:
                weight = cls.PRIORITY_WEIGHTS.get(getattr(task, 'priority', 'MEDIUM'), 1.0)
                hours = float(getattr(task, 'estimated_hours', 5.0) or 5.0)
                total_est_hours += hours

                # Deadline factor
                days_left = (task.due_date - today).days if task.due_date else 14
                if days_left <= 0:
                    urgency_factor = 2.0  # Overdue or due today
                elif days_left <= 3:
                    urgency_factor = 1.5
                elif days_left <= 7:
                    urgency_factor = 1.2
                else:
                    urgency_factor = 1.0

                weighted_workload_sum += (hours * weight * urgency_factor)

            # Project allocations
            proj_count = employee.projects.filter(status='ACTIVE').count() if hasattr(employee, 'projects') else 0

            # Scale to 0-100 index (assuming 40 weighted units is nominal ~75% capacity)
            raw_score = (weighted_workload_sum / 45.0) * 75.0 + (overdue_count * 5.0) + (proj_count * 3.0)
            score = min(100, max(0, round(raw_score)))
            est_hours = Decimal(str(round(total_est_hours, 1)))

        # Determine status
        if score < 35:
            status = UtilizationStatus.UNDERUTILIZED
        elif score <= 75:
            status = UtilizationStatus.BALANCED
        elif score <= 88:
            status = UtilizationStatus.OPTIMAL
        else:
            status = UtilizationStatus.OVERLOADED

        metric, _ = EmployeeWorkloadMetric.objects.update_or_create(
            employee=employee,
            defaults={
                'workload_score': score,
                'active_tasks_count': active_count,
                'estimated_task_hours': est_hours,
                'project_allocation_count': proj_count,
                'overdue_tasks_count': overdue_count,
                'utilization_status': status,
            }
        )

        WorkloadHistory.objects.create(
            employee=employee,
            workload_score=score,
            active_tasks_count=active_count
        )
        return metric

    @classmethod
    def recalculate_all(cls):
        employees = Employee.objects.filter(employment_status='ACTIVE')
        results = []
        for emp in employees:
            metric = cls.calculate_for_employee(emp)
            results.append(metric)
        return results

    recalculate_all_workloads = recalculate_all
