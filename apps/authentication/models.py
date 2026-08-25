import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.permissions.models import SystemRole


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=20, 
        choices=SystemRole.choices, 
        default=SystemRole.EMPLOYEE,
        help_text=_('Designated platform role governing access control')
    )
    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    last_password_change = models.DateTimeField(null=True, blank=True)
    force_password_change = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_locked(self):
        return bool(self.locked_until and self.locked_until > timezone.now())

    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=['failed_login_attempts', 'locked_until'])

    def register_failed_attempt(self, max_attempts=5, lockout_minutes=15):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            self.locked_until = timezone.now() + timezone.timedelta(minutes=lockout_minutes)
        self.save(update_fields=['failed_login_attempts', 'locked_until'])


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='login_history')
    username_attempted = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed'), ('LOCKED', 'Account Locked')])
    failure_reason = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Login History')
        verbose_name_plural = _('Login Histories')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.username_attempted} - {self.status} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    @classmethod
    def generate_token(cls, user, validity_hours=24):
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timezone.timedelta(hours=validity_hours)
        return cls.objects.create(user=user, token=token, expires_at=expires_at)

    @property
    def is_valid(self):
        return (not self.is_used) and (self.expires_at > timezone.now())
