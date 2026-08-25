from django.db import models
from django.utils.translation import gettext_lazy as _


class OrganizationProfile(models.Model):
    name = models.CharField(max_length=200, default="Enterprise Corp Ltd.")
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    registration_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(default="contact@enterprisecorp.internal")
    phone = models.CharField(max_length=30, default="+1 (555) 019-2834")
    website = models.URLField(default="https://ems.enterprisecorp.internal")
    address = models.TextField(default="100 Technology Park, Suite 400")
    city = models.CharField(max_length=100, default="Metropolis")
    state = models.CharField(max_length=100, default="NY")
    country = models.CharField(max_length=100, default="United States")
    postal_code = models.CharField(max_length=20, default="10001")
    currency = models.CharField(max_length=10, default="USD")
    fiscal_year_start_month = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = _('Organization Profile')
        verbose_name_plural = _('Organization Profiles')

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    head_of_department = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )
    budget = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    location = models.CharField(max_length=100, default="HQ Floor 3")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def total_employees(self):
        return self.employees.filter(employment_status='ACTIVE').count()


class Team(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teams')
    team_lead = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_teams'
    )
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        ordering = ['department', 'name']

    def __str__(self):
        return f"{self.name} - {self.department.name}"

    @property
    def total_members(self):
        return self.members.filter(employment_status='ACTIVE').count()


class Designation(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='designations')
    grade_level = models.CharField(max_length=10, default="L3", help_text="e.g. L1, L2, L3, Senior, Principal")
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, default=50000.00)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, default=120000.00)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Designation')
        verbose_name_plural = _('Designations')
        ordering = ['department', 'title']

    def __str__(self):
        return f"{self.title} ({self.code})"
