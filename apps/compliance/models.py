from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee

class StatutoryRegister(models.Model):
    REGISTER_TYPES = [
        ('FORM_A', 'Form A - Employee Register (Maternity / Wages)'),
        ('FORM_B', 'Form B - Wage Register & Overtime Records'),
        ('FORM_C', 'Form C - Loan and Advance Deductions'),
        ('FORM_D', 'Form D - Bonus & Gratuity Calculation Register'),
        ('FACTORY_ACT', 'Factories Act / Shops & Establishment Inspection Register'),
    ]

    title = models.CharField(max_length=200)
    register_type = models.CharField(max_length=50, choices=REGISTER_TYPES)
    period_year = models.IntegerField(default=2026)
    period_month = models.IntegerField(default=8)
    verified_by_officer = models.CharField(max_length=150, default="Priya Patel, Lead Compliance Officer")
    is_signed = models.BooleanField(default=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    document_file = models.FileField(upload_to='compliance_registers/', null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_register_type_display()} - {self.period_year}/{self.period_month}"


class ComplianceAudit(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Q3 Statutory Labor Audit 2026")
    audit_date = models.DateField(default=timezone.now)
    auditor_agency = models.CharField(max_length=150, default="KPMG Internal Audit Advisory")
    lead_auditor = models.CharField(max_length=150, default="Vikramaditya Sengupta")
    score_percentage = models.IntegerField(default=98, help_text="Audit compliance score %")
    status = models.CharField(max_length=30, choices=[('PLANNED', 'Planned'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed & Certified'), ('ACTION_REQUIRED', 'Remediation Required')], default='COMPLETED')
    findings_count = models.IntegerField(default=2)
    summary_report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit: {self.title} ({self.score_percentage}% Pass)"


class POSHCommitteeMember(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='posh_roles')
    role_title = models.CharField(max_length=100, choices=[('PRESIDING_OFFICER', 'Presiding Officer (Senior Woman Leader)'), ('INTERNAL_MEMBER', 'Internal Committee Member'), ('EXTERNAL_NGO_MEMBER', 'External Legal / NGO Specialist')], default='INTERNAL_MEMBER')
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"POSH IC: {self.employee.full_name} ({self.get_role_title_display()})"


class POSHCase(models.Model):
    case_number = models.CharField(max_length=50, unique=True)
    incident_date = models.DateField()
    reported_date = models.DateField(default=timezone.now)
    is_confidential = models.BooleanField(default=True)
    status = models.CharField(max_length=30, choices=[('REPORTED', 'Case Registered'), ('INQUIRY_ONGOING', 'Inquiry Committee Convened'), ('HEARING', 'Hearing & Evidence'), ('REPORT_SUBMITTED', 'Final Report Submitted'), ('CLOSED', 'Closed & Resolved')], default='CLOSED')
    inquiry_findings = models.TextField(help_text="Protected confidential findings")
    action_taken = models.TextField()
    resolved_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case: {self.case_number} - Status: {self.status}"


class PolicyAcknowledgment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='policy_acknowledgments')
    policy_name = models.CharField(max_length=150, help_text="e.g. Code of Business Conduct 2026, Information Security Policy")
    version = models.CharField(max_length=20, default="v3.2")
    acknowledged_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(default="127.0.0.1")
    is_compliant = models.BooleanField(default=True)

    class Meta:
        unique_together = ('employee', 'policy_name', 'version')

    def __str__(self):
        return f"{self.employee.full_name} -> Acknowledged {self.policy_name}"
