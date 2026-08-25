from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee
from apps.projects.models import Project

class ClientRateCard(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rate_cards')
    role_name = models.CharField(max_length=150, help_text="e.g. Lead Architect, Senior Fullstack Engineer")
    hourly_billable_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('85.00'))
    currency = models.CharField(max_length=10, default="USD")
    effective_start = models.DateField()
    effective_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.project.name} - {self.role_name} ({self.currency} {self.hourly_billable_rate}/hr)"


class WeeklyTimesheet(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft / Editing'), ('SUBMITTED', 'Submitted to Manager'), ('APPROVED', 'Approved by Manager'), ('REJECTED', 'Rejected / Revisions Requested')]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='weekly_timesheets')
    week_start_date = models.DateField(help_text="Monday date of the week")
    week_end_date = models.DateField(help_text="Sunday date of the week")
    total_billable_hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('40.00'))
    total_non_billable_hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    approver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_timesheets')
    approver_comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'week_start_date')
        ordering = ['-week_start_date']

    def __str__(self):
        return f"Timesheet: {self.employee.full_name} ({self.week_start_date} to {self.week_end_date}) [{self.status}]"

    @property
    def total_hours(self):
        return self.total_billable_hours + self.total_non_billable_hours


class TimesheetEntry(models.Model):
    timesheet = models.ForeignKey(WeeklyTimesheet, on_delete=models.CASCADE, related_name='entries')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    entry_date = models.DateField()
    hours_logged = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('8.00'))
    is_billable = models.BooleanField(default=True)
    task_description = models.TextField(help_text="Detailed summary of deliverables worked on")
    jira_or_ticket_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.entry_date} - {self.project.name} ({self.hours_logged} hrs)"
