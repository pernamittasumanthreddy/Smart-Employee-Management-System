from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EnrollmentStatus(models.TextChoices):
    ENROLLED = 'ENROLLED', _('Enrolled')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    COMPLETED = 'COMPLETED', _('Completed')
    FAILED = 'FAILED', _('Failed')

class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(
        'skills.SkillCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    provider = models.CharField(max_length=150, default="Internal Academy")
    description = models.TextField(blank=True, null=True)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=1, default=10.0)
    pass_score = models.PositiveIntegerField(default=70, help_text="Minimum pass score percentage")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.code})"


class TrainingEnrollment(models.Model):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='training_enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrollment_date = models.DateField(default=timezone.now)
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.ENROLLED
    )
    score = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    certificate_file = models.FileField(upload_to='training/certificates/', blank=True, null=True)
    certificate_expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _('Training Enrollment')
        verbose_name_plural = _('Training Enrollments')
        unique_together = ('employee', 'course')
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.employee.full_name} -> {self.course.title} ({self.get_status_display()})"

    @property
    def is_expired(self):
        if self.certificate_expiry_date:
            return self.certificate_expiry_date < timezone.now().date()
        return False
