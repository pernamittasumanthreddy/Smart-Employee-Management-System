from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class GoalStatus(models.TextChoices):
    NOT_STARTED = 'NOT_STARTED', _('Not Started')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    ACHIEVED = 'ACHIEVED', _('Achieved')
    MISSED = 'MISSED', _('Missed')
    CANCELLED = 'CANCELLED', _('Cancelled')

class Goal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='goals',
        null=True,
        blank=True,
        help_text="Leave blank if this is a Team-level Goal"
    )
    team = models.ForeignKey(
        'organization.Team',
        on_delete=models.CASCADE,
        related_name='team_goals',
        null=True,
        blank=True
    )
    target_metric = models.CharField(max_length=100, default="Key Deliverables Completed", help_text="e.g. Revenue generated, bugs resolved, certification earned")
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    target_value = models.DecimalField(max_digits=10, decimal_places=2, default=100.0)
    unit = models.CharField(max_length=30, default="Percentage (%)")
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField(db_index=True)
    progress_percentage = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=GoalStatus.choices,
        default=GoalStatus.IN_PROGRESS
    )
    manager_feedback = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_goals'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        if 'target_date' in kwargs and 'due_date' not in kwargs:
            kwargs['due_date'] = kwargs.pop('target_date')
        super().__init__(*args, **kwargs)

    @property
    def target_date(self):
        return self.due_date

    @target_date.setter
    def target_date(self, val):
        self.due_date = val

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')
        ordering = ['due_date']


    def __str__(self):
        owner = self.employee.full_name if self.employee else f"Team {self.team.name}"
        return f"[{owner}] {self.title} ({self.progress_percentage}%)"

    @property
    def is_overdue(self):
        if self.status != GoalStatus.ACHIEVED and self.due_date:
            return self.due_date < timezone.now().date()
        return False
