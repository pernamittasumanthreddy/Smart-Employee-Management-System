from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TaskPriority(models.TextChoices):
    URGENT = 'URGENT', _('Urgent')
    HIGH = 'HIGH', _('High')
    MEDIUM = 'MEDIUM', _('Medium')
    LOW = 'LOW', _('Low')

class TaskStatus(models.TextChoices):
    TODO = 'TODO', _('To Do')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    REVIEW = 'REVIEW', _('In Review')
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELLED = 'CANCELLED', _('Cancelled')

class Task(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=30, unique=True, db_index=True)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    created_by = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_tasks'
    )
    priority = models.CharField(
        max_length=20,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO
    )
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField(db_index=True)
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=1, default=4.0)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    completion_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['due_date', '-priority']

    def __str__(self):
        return f"[{self.code}] {self.title}"

    @property
    def is_overdue(self):
        if self.status != TaskStatus.COMPLETED and self.due_date:
            return self.due_date < timezone.now().date()
        return False


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Subtask')
        verbose_name_plural = _('Subtasks')
        ordering = ['id']

    def __str__(self):
        return f"{self.task.code} - {self.title}"


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='task_comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Task Comment')
        verbose_name_plural = _('Task Comments')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.full_name} on {self.task.code}"


# Alias for backward compatibility
Subtask = SubTask

