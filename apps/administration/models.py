from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditAction(models.TextChoices):
    CREATE = 'CREATE', _('Create Record')
    READ = 'READ', _('Read / Access')
    UPDATE = 'UPDATE', _('Update Record')
    DELETE = 'DELETE', _('Delete Record')
    APPROVE = 'APPROVE', _('Approve Request')
    REJECT = 'REJECT', _('Reject Request')
    LOGIN = 'LOGIN', _('User Login')
    LOGOUT = 'LOGOUT', _('User Logout')
    SECURITY = 'SECURITY', _('Security Event')

class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    username = models.CharField(max_length=150, blank=True, null=True)
    action = models.CharField(max_length=20, choices=AuditAction.choices, db_index=True)
    module = models.CharField(max_length=50, db_index=True)
    record_id = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.username or (self.user.username if self.user else "System")
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {user_str} - {self.action} on {self.module}"


class SecurityEvent(models.Model):
    event_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')])
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Security Event')
        verbose_name_plural = _('Security Events')
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.severity}] {self.event_type} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, default='GENERAL', choices=[
        ('GENERAL', 'General Configuration'),
        ('SECURITY', 'Security & Sessions'),
        ('ATTENDANCE', 'Attendance Rules'),
        ('LEAVE', 'Leave Policies'),
        ('NOTIFICATIONS', 'Notification Preferences'),
    ])

    class Meta:
        verbose_name = _('System Setting')
        verbose_name_plural = _('System Settings')
        ordering = ['category', 'key']

    def __str__(self):
        return f"{self.key} = {self.value}"


class BackupConfiguration(models.Model):
    backup_type = models.CharField(max_length=50, default='FULL_DATABASE_BACKUP')
    frequency = models.CharField(max_length=30, default='DAILY_MIDNIGHT')
    storage_location = models.CharField(max_length=255, default='local_backups/database/')
    last_backup_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, default='CONFIGURED_AND_HEALTHY')
    retention_days = models.PositiveIntegerField(default=30)

    class Meta:
        verbose_name = _('Backup Configuration')
        verbose_name_plural = _('Backup Configurations')

    def __str__(self):
        return f"{self.backup_type} ({self.status})"
