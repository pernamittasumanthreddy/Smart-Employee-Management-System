from datetime import time

from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkShift(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    start_time = models.TimeField(default=time(9, 0))
    end_time = models.TimeField(default=time(17, 30))
    grace_period_minutes = models.PositiveIntegerField(default=15, help_text="Allowed late check-in before penalty")
    half_day_hours = models.DecimalField(max_digits=4, decimal_places=2, default=4.0)
    full_day_hours = models.DecimalField(max_digits=4, decimal_places=2, default=8.0)
    is_night_shift = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Work Shift')
        verbose_name_plural = _('Work Shifts')
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class ShiftAssignment(models.Model):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='shift_assignments'
    )
    shift = models.ForeignKey(
        WorkShift,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Shift Assignment')
        verbose_name_plural = _('Shift Assignments')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee.full_name} -> {self.shift.name}"


class CompanyHoliday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(db_index=True)
    description = models.TextField(blank=True, null=True)
    is_optional = models.BooleanField(default=False)
    department = models.ForeignKey(
        'organization.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Leave blank for all departments"
    )

    class Meta:
        verbose_name = _('Company Holiday')
        verbose_name_plural = _('Company Holidays')
        ordering = ['date']

    def __str__(self):
        return f"{self.name} ({self.date})"


# Alias for backward compatibility
Shift = WorkShift

