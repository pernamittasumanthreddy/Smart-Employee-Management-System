from django.db import models
from django.utils.translation import gettext_lazy as _


class InsightCategory(models.TextChoices):
    ATTENDANCE = 'ATTENDANCE', _('Attendance & Punctuality')
    WORKLOAD = 'WORKLOAD', _('Workload & Capacity')
    SKILL = 'SKILL', _('Skills & Staffing')
    GOAL = 'GOAL', _('Goals & OKRs')
    PERFORMANCE = 'PERFORMANCE', _('Performance & Appraisals')
    TRAINING = 'TRAINING', _('Training & Certifications')
    MANAGER = 'MANAGER', _('Team Manager Intelligence')

class InsightSeverity(models.TextChoices):
    HIGH = 'HIGH', _('High Priority / Critical')
    MEDIUM = 'MEDIUM', _('Medium Priority / Notice')
    LOW = 'LOW', _('Low Priority / Info')
    POSITIVE = 'POSITIVE', _('Positive Achievement / Trend')

class SmartInsight(models.Model):
    category = models.CharField(
        max_length=30,
        choices=InsightCategory.choices,
        db_index=True
    )
    severity = models.CharField(
        max_length=20,
        choices=InsightSeverity.choices,
        default=InsightSeverity.MEDIUM
    )
    title = models.CharField(max_length=200)
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='smart_insights',
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        'organization.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_insights'
    )
    what_detected = models.TextField()
    why_detected = models.TextField(help_text="Mathematical / statistical explanation (e.g. standard deviations, rolling averages)")
    supporting_data = models.JSONField(default=dict, blank=True)
    recommendation = models.TextField()
    confidence_score = models.DecimalField(max_digits=4, decimal_places=2, default=0.90)
    is_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Smart Insight')
        verbose_name_plural = _('Smart Insights')
        ordering = ['-created_at']

    def __str__(self):
        target = self.employee.full_name if self.employee else (self.department.name if self.department else "System")
        return f"[{self.get_category_display()}] {self.title} ({target})"
