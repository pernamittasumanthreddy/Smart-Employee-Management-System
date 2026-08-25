from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EmploymentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', _('Active')
    ON_LEAVE = 'ON_LEAVE', _('On Leave')
    PROBATION = 'PROBATION', _('Probation')
    NOTICE_PERIOD = 'NOTICE_PERIOD', _('Notice Period')
    RESIGNED = 'RESIGNED', _('Resigned')
    TERMINATED = 'TERMINATED', _('Terminated')

class EmploymentType(models.TextChoices):
    FULL_TIME = 'FULL_TIME', _('Full-Time Permanent')
    PART_TIME = 'PART_TIME', _('Part-Time')
    CONTRACT = 'CONTRACT', _('Contractor')
    INTERN = 'INTERN', _('Intern')

class Gender(models.TextChoices):
    MALE = 'MALE', _('Male')
    FEMALE = 'FEMALE', _('Female')
    OTHER = 'OTHER', _('Other')
    PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', _('Prefer not to say')

def employee_photo_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'employees/photos/{instance.employee_id}_{instance.first_name}.{ext}'

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    employee_id = models.CharField(max_length=30, unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    personal_email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, default='')
    
    # Personal & Demographic Details
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, default=Gender.PREFER_NOT_TO_SAY)
    marital_status = models.CharField(max_length=20, choices=[('SINGLE', 'Single'), ('MARRIED', 'Married'), ('DIVORCED', 'Divorced'), ('OTHER', 'Other')], default='SINGLE')
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    national_id = models.CharField(max_length=50, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Address Info
    current_address = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, default='New York')
    state = models.CharField(max_length=100, default='NY')
    country = models.CharField(max_length=100, default='United States')
    postal_code = models.CharField(max_length=20, default='10001')

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=25, blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True, null=True)

    # Organizational Placement
    date_of_joining = models.DateField(default=timezone.now)

    department = models.ForeignKey(
        'organization.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )
    team = models.ForeignKey(
        'organization.Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
    designation = models.ForeignKey(
        'organization.Designation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='holders'
    )
    reporting_manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='direct_reports'
    )

    employment_status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME
    )
    profile_photo = models.ImageField(upload_to=employee_photo_upload_path, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def initials(self):
        fn = self.first_name[0].upper() if self.first_name else ''
        ln = self.last_name[0].upper() if self.last_name else ''
        return f"{fn}{ln}" or "EM"


class EmployeeEducation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=150)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    grade_or_gpa = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _('Employee Education')
        verbose_name_plural = _('Employee Educations')
        ordering = ['-end_year']

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class EmployeeExperience(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Employee Experience')
        verbose_name_plural = _('Employee Experiences')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class EmployeeBankDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='bank_details')
    bank_name = models.CharField(max_length=150)
    account_number = models.CharField(max_length=50)
    routing_or_ifsc_code = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=150, blank=True, null=True)
    account_type = models.CharField(max_length=20, default='SAVINGS', choices=[('SAVINGS', 'Savings'), ('CHECKING', 'Checking'), ('SALARY', 'Salary')])

    class Meta:
        verbose_name = _('Employee Bank Detail')
        verbose_name_plural = _('Employee Bank Details')

    def __str__(self):
        return f"{self.employee.full_name} - {self.bank_name}"
