from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class AttendanceStatus(models.TextChoices):
    PRESENT = 'PRESENT', _('Present')
    ABSENT = 'ABSENT', _('Absent')
    HALF_DAY = 'HALF_DAY', _('Half Day')
    ON_LEAVE = 'ON_LEAVE', _('On Leave')
    HOLIDAY = 'HOLIDAY', _('Holiday')
    WEEKLY_OFF = 'WEEKLY_OFF', _('Weekly Off')

class AttendanceRecord(models.Model):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField(db_index=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    total_working_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.ABSENT
    )
    is_late = models.BooleanField(default=False)
    late_minutes = models.PositiveIntegerField(default=0)
    is_early_departure = models.BooleanField(default=False)
    early_minutes = models.PositiveIntegerField(default=0)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Attendance Record')
        verbose_name_plural = _('Attendance Records')
        unique_together = ('employee', 'date')
        ordering = ['-date', 'employee__first_name']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.get_status_display()})"

    def calculate_hours(self):
        if self.check_in_time and self.check_out_time:
            dummy_date = datetime(2026, 1, 1)
            in_dt = datetime.combine(dummy_date, self.check_in_time)
            out_dt = datetime.combine(dummy_date, self.check_out_time)
            if out_dt > in_dt:
                diff = out_dt - in_dt
                hours = diff.total_seconds() / 3600.0
                self.total_working_hours = round(hours, 2)
                
                # If working hours >= 7.5, marked Present; between 4 and 7.5 -> Half Day; else Absent
                if self.total_working_hours >= 7.5:
                    self.status = AttendanceStatus.PRESENT
                elif self.total_working_hours >= 4.0:
                    self.status = AttendanceStatus.HALF_DAY
                else:
                    self.status = AttendanceStatus.ABSENT
        self.save()
