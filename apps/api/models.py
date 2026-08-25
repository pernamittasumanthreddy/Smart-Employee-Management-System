import secrets
from django.db import models
from django.conf import settings
from django.utils import timezone

class APIKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100, help_text="e.g. Biometric Attendance Sync Service, Mobile App Gateway")
    key = models.CharField(max_length=64, unique=True, default=secrets.token_hex)
    is_active = models.BooleanField(default=True)
    rate_limit_per_minute = models.IntegerField(default=120)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.key[:8]}...)"


class WebhookEndpoint(models.Model):
    name = models.CharField(max_length=150)
    target_url = models.URLField()
    secret_token = models.CharField(max_length=64, default=secrets.token_hex)
    is_active = models.BooleanField(default=True)
    events_subscribed = models.TextField(default="employee.created,leave.approved,attendance.punch,payroll.disbursed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Webhook: {self.name} -> {self.target_url}"


class BiometricDeviceLog(models.Model):
    device_id = models.CharField(max_length=50, default="ZKTECO-GATE-01")
    biometric_user_id = models.CharField(max_length=50)
    punch_timestamp = models.DateTimeField(default=timezone.now)
    punch_type = models.CharField(max_length=20, choices=[('IN', 'Punch In'), ('OUT', 'Punch Out')], default='IN')
    is_synced = models.BooleanField(default=True)
    synced_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Biometric Punch: {self.biometric_user_id} @ {self.punch_timestamp}"
