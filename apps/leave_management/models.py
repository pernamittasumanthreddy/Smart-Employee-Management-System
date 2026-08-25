from django.db import models
from django.utils.translation import gettext_lazy as _


class LeaveStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending Approval')
    APPROVED = 'APPROVED', _('Approved')
    REJECTED = 'REJECTED', _('Rejected')
    CANCELLED = 'CANCELLED', _('Cancelled')

class LeaveType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    days_per_year = models.DecimalField(max_digits=5, decimal_places=1, default=12.0)
    is_carry_forward = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Leave Type')
        verbose_name_plural = _('Leave Types')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class LeaveBalance(models.Model):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='balances'
    )
    year = models.PositiveIntegerField(default=2026)
    total_allocated = models.DecimalField(max_digits=5, decimal_places=1, default=12.0)
    used_days = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    pending_days = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)

    class Meta:
        verbose_name = _('Leave Balance')
        verbose_name_plural = _('Leave Balances')
        unique_together = ('employee', 'leave_type', 'year')

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type.name}: {self.remaining_days} days left"

    @property
    def remaining_days(self):
        return max(0.0, float(self.total_allocated - self.used_days - self.pending_days))


class LeaveRequest(models.Model):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=LeaveStatus.choices,
        default=LeaveStatus.PENDING
    )
    reviewed_by = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_leaves'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='leaves/attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Leave Request')
        verbose_name_plural = _('Leave Requests')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type.code} ({self.start_date} to {self.end_date})"
