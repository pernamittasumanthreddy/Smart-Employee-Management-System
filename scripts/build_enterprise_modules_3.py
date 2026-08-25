import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# 3. APPS / LIFECYCLE (Onboarding, Offboarding, Clearances)
# ==============================================================================

write_file("apps/lifecycle/__init__.py", """default_app_config = 'apps.lifecycle.apps.LifecycleConfig'""")

write_file("apps/lifecycle/apps.py", """
from django.apps import AppConfig

class LifecycleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.lifecycle'
    verbose_name = 'Employee Lifecycle, Onboarding & Exit Clearances'
""")

write_file("apps/lifecycle/models.py", """
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee

class OnboardingWorkflow(models.Model):
    STATUS_CHOICES = [('INITIATED', 'Initiated / In Progress'), ('VERIFICATION', 'Document Verification'), ('COMPLETED', 'Onboarding Complete'), ('CANCELLED', 'Offer Rescinded')]

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='onboarding_workflow')
    mentor_buddy = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentored_onboardings')
    joining_date = models.DateField(default=timezone.now)
    probation_period_months = models.IntegerField(default=6)
    probation_end_date = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='INITIATED')
    welcome_email_sent = models.BooleanField(default=False)
    it_assets_assigned = models.BooleanField(default=False)
    hr_orientation_completed = models.BooleanField(default=False)
    id_badge_issued = models.BooleanField(default=False)
    bank_details_verified = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Onboarding: {self.employee.full_name} ({self.status})"

    @property
    def progress_percentage(self):
        checks = [self.welcome_email_sent, self.it_assets_assigned, self.hr_orientation_completed, self.id_badge_issued, self.bank_details_verified]
        return int((sum(1 for c in checks if c) / len(checks)) * 100)


class OnboardingTask(models.Model):
    workflow = models.ForeignKey(OnboardingWorkflow, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=[('IT_SETUP', 'IT & System Setup'), ('HR_DOCS', 'HR Documentation'), ('TRAINING', 'Initial Training & Compliance'), ('TEAM', 'Team Introductions & 1-on-1s')], default='HR_DOCS')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.workflow.employee.full_name}"


class ProbationReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='probation_reviews')
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='conducted_probation_reviews')
    review_date = models.DateField(default=timezone.now)
    performance_score = models.IntegerField(choices=[(1, '1-Unsatisfactory'), (2, '2-Needs Improvement'), (3, '3-Meets Expectations'), (4, '4-Exceeds Expectations'), (5, '5-Outstanding')], default=4)
    culture_fit_score = models.IntegerField(choices=[(1, '1-Poor'), (2, '2-Fair'), (3, '3-Good'), (4, '4-Very Good'), (5, '5-Exceptional')], default=4)
    attendance_score = models.IntegerField(choices=[(1, '1-Poor'), (2, '2-Fair'), (3, '3-Good'), (4, '4-Very Good'), (5, '5-Exceptional')], default=5)
    decision = models.CharField(max_length=30, choices=[('CONFIRM', 'Confirm Employment (Regularize)'), ('EXTEND', 'Extend Probation by 3 Months'), ('TERMINATE', 'Terminate / End Association')], default='CONFIRM')
    manager_feedback = models.TextField()
    is_approved_by_hr = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Probation Review: {self.employee.full_name} -> {self.decision}"


class ResignationRequest(models.Model):
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted by Employee'),
        ('MANAGER_REVIEW', 'Under Manager Review'),
        ('ACCEPTED', 'Accepted & Notice Period Active'),
        ('CLEARANCE', 'In Clearance & Handover Phase'),
        ('RELIEVED', 'Relieved / Completed Exit'),
        ('WITHDRAWN', 'Resignation Withdrawn'),
        ('REJECTED', 'Rejected / Retention Agreed'),
    ]

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='resignation_request')
    resignation_date = models.DateField(default=timezone.now)
    proposed_last_working_day = models.DateField()
    approved_last_working_day = models.DateField(null=True, blank=True)
    reason_category = models.CharField(max_length=50, choices=[('BETTER_OPPORTUNITY', 'Higher Studies / Better Opportunity'), ('CAREER_CHANGE', 'Career Change'), ('COMPENSATION', 'Compensation / Benefits'), ('PERSONAL', 'Personal / Family Relocation'), ('HEALTH', 'Health Reasons'), ('OTHER', 'Other')], default='BETTER_OPPORTUNITY')
    detailed_reason = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUBMITTED')
    manager_comments = models.TextField(blank=True)
    hr_exit_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resignation: {self.employee.full_name} ({self.get_status_display()})"


class DepartmentClearance(models.Model):
    resignation = models.ForeignKey(ResignationRequest, on_delete=models.CASCADE, related_name='clearances')
    department_name = models.CharField(max_length=50, choices=[('IT', 'IT Infrastructure & Hardware Return'), ('FINANCE', 'Finance, Loans & Travel Advances'), ('ADMIN', 'Admin, Access Cards & Lockers'), ('HR', 'HR, Medical Insurance & Documentation'), ('REPORTING_MANAGER', 'Reporting Manager Knowledge Handover')])
    cleared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_cleared = models.BooleanField(default=False)
    cleared_at = models.DateTimeField(null=True, blank=True)
    pending_items = models.TextField(blank=True, help_text="e.g. Laptop, Charger, YubiKey, ID Card")
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('resignation', 'department_name')

    def __str__(self):
        return f"Clearance: {self.resignation.employee.full_name} - {self.department_name} ({'Cleared' if self.is_cleared else 'Pending'})"


class ExperienceCertificate(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='experience_certificates')
    certificate_number = models.CharField(max_length=50, unique=True)
    issued_date = models.DateField(default=timezone.now)
    last_designation = models.CharField(max_length=150)
    joining_date = models.DateField()
    relieving_date = models.DateField()
    conduct_remarks = models.CharField(max_length=100, default="Exemplary and Professional")
    authorized_signatory_name = models.CharField(max_length=150, default="Aarav Sharma, Chief People Officer")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Experience Cert: {self.certificate_number} ({self.employee.full_name})"
""")

write_file("apps/lifecycle/views.py", """
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.lifecycle.models import OnboardingWorkflow, OnboardingTask, ProbationReview, ResignationRequest, DepartmentClearance, ExperienceCertificate
from apps.employees.models import Employee

@login_required
def lifecycle_dashboard(request):
    onboardings = OnboardingWorkflow.objects.select_related('employee', 'mentor_buddy').all()[:8]
    resignations = ResignationRequest.objects.select_related('employee').all()[:8]
    pending_probations = ProbationReview.objects.filter(is_approved_by_hr=False).select_related('employee', 'reviewer')
    
    context = {
        'onboardings': onboardings,
        'resignations': resignations,
        'pending_probations': pending_probations,
    }
    return render(request, 'lifecycle/dashboard.html', context)

@login_required
def onboarding_list(request):
    onboardings = OnboardingWorkflow.objects.select_related('employee', 'mentor_buddy')
    return render(request, 'lifecycle/onboarding_list.html', {'onboardings': onboardings})

@login_required
def onboarding_detail(request, pk):
    workflow = get_object_or_404(OnboardingWorkflow.objects.select_related('employee'), pk=pk)
    tasks = workflow.tasks.all()
    return render(request, 'lifecycle/onboarding_detail.html', {'workflow': workflow, 'tasks': tasks})

@login_required
def resignation_list(request):
    resignations = ResignationRequest.objects.select_related('employee')
    return render(request, 'lifecycle/resignation_list.html', {'resignations': resignations})

@login_required
def resignation_detail(request, pk):
    resignation = get_object_or_404(ResignationRequest.objects.select_related('employee'), pk=pk)
    clearances = resignation.clearances.all()
    return render(request, 'lifecycle/resignation_detail.html', {'resignation': resignation, 'clearances': clearances})

@login_required
def certificate_view(request, pk):
    cert = get_object_or_404(ExperienceCertificate.objects.select_related('employee'), pk=pk)
    return render(request, 'lifecycle/experience_certificate.html', {'cert': cert})
""")

write_file("apps/lifecycle/urls.py", """
from django.urls import path
from apps.lifecycle import views

app_name = 'lifecycle'

urlpatterns = [
    path('', views.lifecycle_dashboard, name='dashboard'),
    path('onboarding/', views.onboarding_list, name='onboarding_list'),
    path('onboarding/<int:pk>/', views.onboarding_detail, name='onboarding_detail'),
    path('resignations/', views.resignation_list, name='resignation_list'),
    path('resignations/<int:pk>/', views.resignation_detail, name='resignation_detail'),
    path('certificates/<int:pk>/', views.certificate_view, name='certificate_view'),
]
""")

write_file("apps/lifecycle/admin.py", """
from django.contrib import admin
from apps.lifecycle.models import OnboardingWorkflow, OnboardingTask, ProbationReview, ResignationRequest, DepartmentClearance, ExperienceCertificate

@admin.register(OnboardingWorkflow)
class OnboardingWorkflowAdmin(admin.ModelAdmin):
    list_display = ('employee', 'joining_date', 'status', 'it_assets_assigned', 'hr_orientation_completed')

@admin.register(ResignationRequest)
class ResignationRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'resignation_date', 'status', 'reason_category')

@admin.register(DepartmentClearance)
class DepartmentClearanceAdmin(admin.ModelAdmin):
    list_display = ('resignation', 'department_name', 'is_cleared', 'cleared_by')

@admin.register(ExperienceCertificate)
class ExperienceCertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'employee', 'issued_date', 'last_designation')
""")

# ==============================================================================
# 4. APPS / COMPLIANCE (Statutory Registers, POSH, Labor Law)
# ==============================================================================

write_file("apps/compliance/__init__.py", """default_app_config = 'apps.compliance.apps.ComplianceConfig'""")

write_file("apps/compliance/apps.py", """
from django.apps import AppConfig

class ComplianceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.compliance'
    verbose_name = 'Enterprise Statutory & Legal Compliance (Labor Law / POSH)'
""")

write_file("apps/compliance/models.py", """
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
""")

write_file("apps/compliance/views.py", """
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.compliance.models import StatutoryRegister, ComplianceAudit, POSHCommitteeMember, POSHCase, PolicyAcknowledgment

@login_required
def compliance_dashboard(request):
    registers = StatutoryRegister.objects.all()[:6]
    audits = ComplianceAudit.objects.all()[:5]
    posh_members = POSHCommitteeMember.objects.filter(is_active=True).select_related('employee')
    total_acks = PolicyAcknowledgment.objects.count()
    
    context = {
        'registers': registers,
        'audits': audits,
        'posh_members': posh_members,
        'total_acks': total_acks,
    }
    return render(request, 'compliance/dashboard.html', context)

@login_required
def register_list(request):
    registers = StatutoryRegister.objects.all()
    return render(request, 'compliance/register_list.html', {'registers': registers})

@login_required
def audit_list(request):
    audits = ComplianceAudit.objects.all()
    return render(request, 'compliance/audit_list.html', {'audits': audits})

@login_required
def posh_portal(request):
    posh_members = POSHCommitteeMember.objects.filter(is_active=True).select_related('employee')
    return render(request, 'compliance/posh_portal.html', {'posh_members': posh_members})
""")

write_file("apps/compliance/urls.py", """
from django.urls import path
from apps.compliance import views

app_name = 'compliance'

urlpatterns = [
    path('', views.compliance_dashboard, name='dashboard'),
    path('registers/', views.register_list, name='register_list'),
    path('audits/', views.audit_list, name='audit_list'),
    path('posh/', views.posh_portal, name='posh_portal'),
]
""")

write_file("apps/compliance/admin.py", """
from django.contrib import admin
from apps.compliance.models import StatutoryRegister, ComplianceAudit, POSHCommitteeMember, POSHCase, PolicyAcknowledgment

@admin.register(StatutoryRegister)
class StatutoryRegisterAdmin(admin.ModelAdmin):
    list_display = ('title', 'register_type', 'period_year', 'period_month', 'is_signed')

@admin.register(ComplianceAudit)
class ComplianceAuditAdmin(admin.ModelAdmin):
    list_display = ('title', 'audit_date', 'score_percentage', 'status')

@admin.register(POSHCommitteeMember)
class POSHCommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('employee', 'role_title', 'contact_email', 'is_active')
""")

# ==============================================================================
# 5. APPS / BENEFITS (Corporate Insurance & Perks)
# ==============================================================================

write_file("apps/benefits/__init__.py", """default_app_config = 'apps.benefits.apps.BenefitsConfig'""")

write_file("apps/benefits/apps.py", """
from django.apps import AppConfig

class BenefitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.benefits'
    verbose_name = 'Corporate Benefits, Health Insurance & Flexi-Perks'
""")

write_file("apps/benefits/models.py", """
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee

class InsurancePolicy(models.Model):
    POLICY_TYPES = [('GMC', 'Group Mediclaim Policy (Family Floater)'), ('GPA', 'Group Personal Accident'), ('GTL', 'Group Term Life Insurance')]

    name = models.CharField(max_length=200, help_text="e.g. Star Health Corporate Floater 5L")
    policy_number = models.CharField(max_length=100, unique=True)
    provider_name = models.CharField(max_length=150, default="ICICI Lombard / Star Health")
    policy_type = models.CharField(max_length=30, choices=POLICY_TYPES, default='GMC')
    sum_insured = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('500000.00'))
    start_date = models.DateField()
    end_date = models.DateField()
    tpa_name = models.CharField(max_length=150, default="Medi Assist TPA Services", help_text="Third Party Administrator")
    tpa_toll_free = models.CharField(max_length=50, default="1800-425-9449")
    cashless_hospitals_count = models.IntegerField(default=12000)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (Coverage: INR {self.sum_insured:,.0f})"


class EmployeeInsuranceEnrollment(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='insurance_enrollment')
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE, related_name='enrollments')
    card_number = models.CharField(max_length=50, unique=True)
    enrolled_date = models.DateField(default=timezone.now)
    sum_insured_allocated = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('500000.00'))
    total_claims_utilized = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Insurance: {self.employee.full_name} ({self.card_number})"

    @property
    def remaining_coverage(self):
        return self.sum_insured_allocated - self.total_claims_utilized


class InsuranceDependent(models.Model):
    RELATION_CHOICES = [('SPOUSE', 'Spouse / Partner'), ('CHILD_1', 'Child 1'), ('CHILD_2', 'Child 2'), ('PARENT_1', 'Father / Mother-in-Law'), ('PARENT_2', 'Mother / Father-in-Law')]

    enrollment = models.ForeignKey(EmployeeInsuranceEnrollment, on_delete=models.CASCADE, related_name='dependents')
    full_name = models.CharField(max_length=150)
    relationship = models.CharField(max_length=30, choices=RELATION_CHOICES)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')])
    health_card_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.get_relationship_display()}) - {self.enrollment.employee.full_name}"


class InsuranceClaim(models.Model):
    STATUS_CHOICES = [('SUBMITTED', 'Submitted to TPA'), ('UNDER_REVIEW', 'Under Document Verification'), ('APPROVED', 'Approved for Cashless/Reimbursement'), ('SETTLED', 'Claim Amount Settled & Paid'), ('REJECTED', 'Claim Rejected by Insurer')]

    enrollment = models.ForeignKey(EmployeeInsuranceEnrollment, on_delete=models.CASCADE, related_name='claims')
    claim_id = models.CharField(max_length=50, unique=True)
    patient_name = models.CharField(max_length=150)
    hospital_name = models.CharField(max_length=200)
    admission_date = models.DateField()
    discharge_date = models.DateField()
    claimed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    diagnosis = models.CharField(max_length=255)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUBMITTED')
    settled_date = models.DateField(null=True, blank=True)
    tpa_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim #{self.claim_id} - {self.patient_name} (INR {self.claimed_amount:,.2f})"


class FlexibleBenefitPlan(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='fbp_plan')
    financial_year = models.CharField(max_length=20, default="2026-2027")
    total_fbp_budget = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('120000.00'))
    meal_card_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('26400.00'))
    fuel_driver_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('30000.00'))
    books_periodicals = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('15000.00'))
    internet_telecom = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('24000.00'))
    gym_wellness_reimbursement = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('24600.00'))
    is_locked = models.BooleanField(default=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FBP: {self.employee.full_name} FY {self.financial_year}"
""")

write_file("apps/benefits/views.py", """
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.benefits.models import InsurancePolicy, EmployeeInsuranceEnrollment, InsuranceDependent, InsuranceClaim, FlexibleBenefitPlan

@login_required
def benefits_dashboard(request):
    policies = InsurancePolicy.objects.filter(is_active=True)
    user_enrollment = None
    user_claims = []
    user_fbp = None
    
    if hasattr(request.user, 'employee_profile'):
        emp = request.user.employee_profile
        try:
            user_enrollment = emp.insurance_enrollment
            user_claims = user_enrollment.claims.all()
        except Exception:
            pass
        try:
            user_fbp = emp.fbp_plan
        except Exception:
            pass

    context = {
        'policies': policies,
        'user_enrollment': user_enrollment,
        'user_claims': user_claims,
        'user_fbp': user_fbp,
    }
    return render(request, 'benefits/dashboard.html', context)

@login_required
def policy_list(request):
    policies = InsurancePolicy.objects.all()
    return render(request, 'benefits/policy_list.html', {'policies': policies})

@login_required
def claims_list(request):
    claims = InsuranceClaim.objects.select_related('enrollment__employee')
    return render(request, 'benefits/claims_list.html', {'claims': claims})
""")

write_file("apps/benefits/urls.py", """
from django.urls import path
from apps.benefits import views

app_name = 'benefits'

urlpatterns = [
    path('', views.benefits_dashboard, name='dashboard'),
    path('policies/', views.policy_list, name='policy_list'),
    path('claims/', views.claims_list, name='claims_list'),
]
""")

write_file("apps/benefits/admin.py", """
from django.contrib import admin
from apps.benefits.models import InsurancePolicy, EmployeeInsuranceEnrollment, InsuranceDependent, InsuranceClaim, FlexibleBenefitPlan

@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'policy_number', 'provider_name', 'sum_insured', 'is_active')

@admin.register(EmployeeInsuranceEnrollment)
class EmployeeInsuranceEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'card_number', 'sum_insured_allocated', 'total_claims_utilized')

@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_id', 'enrollment', 'claimed_amount', 'approved_amount', 'status')
    list_filter = ('status',)
""")

print("Finished Lifecycle, Compliance, and Benefits modules generation.")
