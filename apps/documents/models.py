from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class DocumentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Document Category')
        verbose_name_plural = _('Document Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class EmployeeDocument(models.Model):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True,
        help_text="Leave blank if this is a company-wide policy/handbook"
    )
    category = models.ForeignKey(
        DocumentCategory,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=200)
    document_number = models.CharField(max_length=100, blank=True, null=True)
    document_file = models.FileField(upload_to='documents/records/')
    expiry_date = models.DateField(null=True, blank=True)
    is_company_wide = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_documents'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Employee Document')
        verbose_name_plural = _('Employee Documents')
        ordering = ['-created_at']

    def __str__(self):
        owner = self.employee.full_name if self.employee else "Company-wide"
        return f"[{owner}] {self.title} ({self.category.name})"

    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False
