from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectStatus(models.TextChoices):
    PLANNING = 'PLANNING', _('Planning')
    ACTIVE = 'ACTIVE', _('Active')
    ON_HOLD = 'ON_HOLD', _('On Hold')
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELLED = 'CANCELLED', _('Cancelled')

class Project(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_projects'
    )
    members = models.ManyToManyField(
        'employees.Employee',
        related_name='projects',
        blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PLANNING
    )
    progress_percentage = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def recalculate_progress(self):
        tasks = self.tasks.all()
        total_tasks = tasks.count()
        if total_tasks > 0:
            completed_tasks = tasks.filter(status='COMPLETED').count()
            self.progress_percentage = round((completed_tasks / total_tasks) * 100)
        else:
            self.progress_percentage = 0
        self.save(update_fields=['progress_percentage'])


class ProjectMilestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _('Project Milestone')
        verbose_name_plural = _('Project Milestones')
        ordering = ['due_date']

    def __str__(self):
        return f"{self.project.code} - {self.title}"
