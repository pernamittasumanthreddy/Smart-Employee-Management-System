from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AnnouncementCategory(models.TextChoices):
    GENERAL = 'GENERAL', _('General Announcement')
    HR_UPDATE = 'HR_UPDATE', _('HR Policy & Updates')
    EVENT = 'EVENT', _('Company Event')
    POLICY_UPDATE = 'POLICY_UPDATE', _('Compliance & Security')
    EMERGENCY = 'EMERGENCY', _('Urgent / Alert')

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(
        max_length=30,
        choices=AnnouncementCategory.choices,
        default=AnnouncementCategory.GENERAL
    )
    target_department = models.ForeignKey(
        'organization.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Leave blank for company-wide distribution"
    )
    publish_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='announcements'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')
        ordering = ['-is_pinned', '-publish_date']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class CompanyEvent(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=150, default="Main Town Hall / Virtual")
    registration_required = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Company Event')
        verbose_name_plural = _('Company Events')
        ordering = ['event_date']

    def __str__(self):
        return f"{self.title} on {self.event_date.strftime('%Y-%m-%d %H:%M')}"


class EventRegistration(models.Model):
    event = models.ForeignKey(
        CompanyEvent,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Event Registration')
        verbose_name_plural = _('Event Registrations')
        unique_together = ('event', 'employee')

    def __str__(self):
        return f"{self.employee.full_name} -> {self.event.title}"
