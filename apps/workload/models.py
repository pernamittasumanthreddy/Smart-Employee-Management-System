from django.db import models
from django.utils.translation import gettext_lazy as _


class UtilizationStatus(models.TextChoices):
    UNDERUTILIZED = 'UNDERUTILIZED', _('Underutilized (<35%)')
    BALANCED = 'BALANCED', _('Balanced (35-75%)')
    OPTIMAL = 'OPTIMAL', _('Optimal (75-85%)')
    OVERLOADED = 'OVERLOADED', _('Overloaded (>85%)')

class EmployeeWorkloadMetric(models.Model):
    employee = models.OneToOneField(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='workload_metric'
    )
    workload_score = models.PositiveIntegerField(default=0, help_text="Normalized workload score from 0 to 100")
    active_tasks_count = models.PositiveIntegerField(default=0)
    estimated_task_hours = models.DecimalField(max_digits=6, decimal_places=1, default=0.0)
    project_allocation_count = models.PositiveIntegerField(default=0)
    overdue_tasks_count = models.PositiveIntegerField(default=0)
    utilization_status = models.CharField(
        max_length=20,
        choices=UtilizationStatus.choices,
        default=UtilizationStatus.BALANCED
    )
    last_calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Employee Workload Metric')
        verbose_name_plural = _('Employee Workload Metrics')
        ordering = ['-workload_score']

    def __str__(self):
        return f"{self.employee.full_name} - Score: {self.workload_score}% ({self.get_utilization_status_display()})"


class WorkloadHistory(models.Model):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='workload_history'
    )
    workload_score = models.PositiveIntegerField()
    active_tasks_count = models.PositiveIntegerField()
    recorded_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _('Workload History')
        verbose_name_plural = _('Workload Histories')
        ordering = ['-recorded_date']

    def __str__(self):
        return f"{self.employee.full_name} ({self.recorded_date}): {self.workload_score}%"


# Alias for backward compatibility
WorkloadMetric = EmployeeWorkloadMetric

