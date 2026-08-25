from django.db import models
from django.conf import settings
from django.utils import timezone

class AutomationRule(models.Model):
    TRIGGER_EVENTS = [
        ('EMPLOYEE_JOINED', 'When a new employee joins (Onboarding)'),
        ('LEAVE_APPROVED', 'When a leave request is approved'),
        ('PROBATION_DUE', 'When employee probation review date arrives'),
        ('WORK_ANNIVERSARY', 'On employee work anniversary milestone'),
        ('BIRTHDAY_ALERT', 'On employee birthday'),
        ('EXPENSE_SUBMITTED', 'When high-value expense claim is filed'),
        ('PAYROLL_PROCESSED', 'When monthly payroll run is completed'),
    ]

    ACTION_TYPES = [
        ('DISPATCH_EMAIL', 'Dispatch Automated Notification Email'),
        ('SEND_IN_APP_ALERT', 'Send Instant In-App System Alert'),
        ('CREATE_TASK', 'Create Follow-up Task for Manager'),
        ('TRIGGER_WEBHOOK', 'Fire Webhook to External ERP / Slack'),
        ('AWARD_KUDOS_BADGE', 'Award Automated Recognition Badge'),
    ]

    name = models.CharField(max_length=200, help_text="e.g. Auto-Welcome Email & Task Generation on Hire")
    trigger_event = models.CharField(max_length=50, choices=TRIGGER_EVENTS)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    action_payload = models.TextField(help_text="JSON or configuration parameters for the action")
    is_active = models.BooleanField(default=True)
    total_executions = models.IntegerField(default=0)
    last_executed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        kwargs.pop('condition_expression', None)
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"Rule: {self.name} [{self.get_trigger_event_display()}]"


class ExecutionLog(models.Model):
    rule = models.ForeignKey(AutomationRule, on_delete=models.CASCADE, related_name='execution_logs')
    executed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('SUCCESS', 'Executed Successfully'), ('FAILED', 'Execution Error'), ('SKIPPED', 'Conditions Not Met')], default='SUCCESS')
    details = models.TextField()

    def __init__(self, *args, **kwargs):
        kwargs.pop('triggered_by_entity', None)
        super().__init__(*args, **kwargs)

    class Meta:
        ordering = ['-executed_at']

    def __str__(self):
        return f"Log: {self.rule.name} @ {self.executed_at} ({self.status})"



# Alias for backward compatibility
AutomationExecutionLog = ExecutionLog

