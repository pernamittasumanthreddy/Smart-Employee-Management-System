from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationCategory(models.TextChoices):
    LEAVE = 'LEAVE', _('Leave')
    TASK = 'TASK', _('Task')
    PROJECT = 'PROJ', _('Project')
    TRAINING = 'TRAIN', _('Training')
    EXPENSE = 'EXP', _('Expense')
    ASSET = 'ASSET', _('Asset')
    DOCUMENT = 'DOC', _('Document')
    HELPDESK = 'HELP', _('Helpdesk')
    ANNOUNCEMENT = 'ANNC', _('Announcement')
    RECOGNITION = 'RECOG', _('Recognition')
    SYSTEM = 'SYSTEM', _('System Alert')

class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=150)
    message = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=NotificationCategory.choices,
        default=NotificationCategory.SYSTEM
    )
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.recipient.username}] {self.title} ({'Read' if self.is_read else 'Unread'})"
