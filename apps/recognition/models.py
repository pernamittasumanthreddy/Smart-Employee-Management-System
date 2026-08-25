from django.db import models
from django.utils.translation import gettext_lazy as _


class RecognitionCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    badge_icon = models.CharField(max_length=50, default='bi-star-fill', help_text='Bootstrap Icon class')
    badge_color = models.CharField(max_length=20, default='#f59e0b')
    points = models.PositiveIntegerField(default=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Recognition Category')
        verbose_name_plural = _('Recognition Categories')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (+{self.points} pts)"


class EmployeeRecognition(models.Model):
    sender = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='recognitions_given'
    )
    recipient = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='recognitions_received'
    )
    category = models.ForeignKey(
        RecognitionCategory,
        on_delete=models.CASCADE,
        related_name='recognitions'
    )
    title = models.CharField(max_length=150)
    message = models.TextField()
    points_awarded = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Employee Recognition')
        verbose_name_plural = _('Employee Recognitions')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.full_name} -> {self.recipient.full_name} [{self.category.name}]"


# Alias for backward compatibility
Recognition = EmployeeRecognition

