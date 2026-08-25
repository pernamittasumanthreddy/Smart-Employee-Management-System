from django.db import models
from django.utils.translation import gettext_lazy as _


class SystemRole(models.TextChoices):
    ADMIN = 'ADMIN', _('Administrator')
    HR = 'HR', _('HR Manager')
    MANAGER = 'MANAGER', _('Team Manager')
    EMPLOYEE = 'EMPLOYEE', _('Employee')

class SystemModule(models.TextChoices):
    AUTHENTICATION = 'AUTH', _('Authentication')
    EMPLOYEE_MANAGEMENT = 'EMP', _('Employee Management')
    ORGANIZATION_MANAGEMENT = 'ORG', _('Organization Management')
    ROLES_PERMISSIONS = 'PERM', _('Roles & Permissions')
    ATTENDANCE_MANAGEMENT = 'ATT', _('Attendance Management')
    LEAVE_MANAGEMENT = 'LEAVE', _('Leave Management')
    SHIFT_HOLIDAY_MANAGEMENT = 'SHIFT', _('Shift & Holiday Management')
    WORKLOAD_MANAGEMENT = 'WORKLOAD', _('Workload Management')
    PROJECT_MANAGEMENT = 'PROJ', _('Project Management')
    TASK_MANAGEMENT = 'TASK', _('Task Management')
    SKILLS_MANAGEMENT = 'SKILL', _('Skills Management')
    GOALS_MANAGEMENT = 'GOAL', _('Goals Management')
    PERFORMANCE_MANAGEMENT = 'PERF', _('Performance Management')
    TRAINING_DEVELOPMENT = 'TRAIN', _('Training & Development')
    RECOGNITION_FEEDBACK = 'RECOG', _('Recognition & Feedback')
    ASSET_MANAGEMENT = 'ASSET', _('Asset Management')
    EXPENSE_MANAGEMENT = 'EXP', _('Expense Management')
    HELPDESK_SUPPORT = 'HELP', _('Helpdesk / Support')
    DOCUMENT_MANAGEMENT = 'DOC', _('Document Management')
    ANNOUNCEMENTS_EVENTS = 'ANNC', _('Announcements & Events')
    NOTIFICATIONS = 'NOTIF', _('Notifications')
    SMART_INSIGHTS = 'INSIGHT', _('Smart Insights')
    REPORTS_ANALYTICS = 'REP', _('Reports & Analytics')
    AUDIT_ADMINISTRATION = 'AUDIT', _('Audit & System Administration')

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, choices=SystemRole.choices, unique=True)
    description = models.TextField(blank=True, null=True)
    is_system_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class ModulePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    module = models.CharField(max_length=30, choices=SystemModule.choices)
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=True)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Module Permission')
        verbose_name_plural = _('Module Permissions')
        unique_together = ('role', 'module')

    def __str__(self):
        return f"{self.role.name} - {self.get_module_display()}"
