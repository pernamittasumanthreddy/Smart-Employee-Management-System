from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class SavedReport(models.Model):
    title = models.CharField(max_length=150)
    report_type = models.CharField(max_length=50, choices=[
        ('EMPLOYEE', 'Employee Headcount Report'),
        ('ATTENDANCE', 'Workforce Attendance Report'),
        ('LEAVE', 'Leave Utilization Report'),
        ('PROJECT', 'Project Progress & Task Tracking'),
        ('PERFORMANCE', 'Performance Analytics & Ratings'),
        ('TRAINING', 'Skill & Training Compliance'),
        ('EXPENSE', 'Expense & Asset Tracking'),
        ('HELPDESK', 'Helpdesk SLA Performance'),
    ])
    filters_applied = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Saved Report')
        verbose_name_plural = _('Saved Reports')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"
