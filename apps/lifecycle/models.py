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
