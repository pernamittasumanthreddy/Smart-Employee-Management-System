from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.organization.models import Department, Designation
from apps.employees.models import Employee

class JobRequisition(models.Model):
    PRIORITY_CHOICES = [('LOW', 'Low Priority'), ('MEDIUM', 'Medium Priority'), ('HIGH', 'High Priority'), ('URGENT', 'Critical / Urgent')]
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted for Approval'), ('APPROVED', 'Approved by Leadership'), ('REJECTED', 'Rejected'), ('CLOSED', 'Fulfilled / Closed')]

    title = models.CharField(max_length=200, help_text="e.g. Senior Cloud Architect, HR Talent Partner")
    requisition_code = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='job_requisitions')
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    headcount = models.PositiveIntegerField(default=1)
    hiring_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_requisitions')
    min_experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('3.0'))
    max_experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('8.0'))
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('800000.00'))
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('1500000.00'))
    employment_type = models.CharField(max_length=50, choices=[('FULL_TIME', 'Full-Time Regular'), ('CONTRACT', 'Contractor'), ('INTERN', 'Internship')], default='FULL_TIME')
    work_location = models.CharField(max_length=150, default="Bengaluru HQ / Hybrid")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='HIGH')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    justification = models.TextField(help_text="Business justification for hiring")
    job_description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated skills e.g. Python, Django, AWS, PostgreSQL")
    target_hire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Requisition'
        verbose_name_plural = 'Job Requisitions'

    def __str__(self):
        return f"{self.title} ({self.requisition_code})"


class JobPosting(models.Model):
    requisition = models.OneToOneField(JobRequisition, on_delete=models.CASCADE, related_name='posting')
    public_slug = models.SlugField(max_length=200, unique=True)
    is_published = models.BooleanField(default=True)
    published_date = models.DateField(default=timezone.now)
    application_deadline = models.DateField()
    views_count = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Posting: {self.requisition.title}"


class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30)
    current_company = models.CharField(max_length=150, blank=True)
    current_designation = models.CharField(max_length=150, blank=True)
    total_experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('4.0'))
    current_ctc = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('900000.00'))
    expected_ctc = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('1200000.00'))
    notice_period_days = models.PositiveIntegerField(default=30)
    current_location = models.CharField(max_length=100, default="Bengaluru")
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    skills_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class JobApplication(models.Model):
    STAGE_CHOICES = [
        ('APPLIED', 'Application Received'),
        ('SCREENING', 'Resume Screened / Shortlisted'),
        ('TECH_INTERVIEW', 'Technical Evaluation'),
        ('MANAGERIAL', 'Managerial & Cultural Fit'),
        ('HR_ROUND', 'HR & Compensation Discussion'),
        ('OFFER_EXTENDED', 'Offer Letter Extended'),
        ('HIRED', 'Joined / Hired'),
        ('REJECTED', 'Not Selected / Rejected'),
        ('WITHDRAWN', 'Candidate Withdrew'),
    ]

    job_requisition = models.ForeignKey(JobRequisition, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    stage = models.CharField(max_length=30, choices=STAGE_CHOICES, default='APPLIED')
    source = models.CharField(max_length=50, choices=[('CAREERS_PORTAL', 'Careers Website'), ('LINKEDIN', 'LinkedIn'), ('EMPLOYEE_REFERRAL', 'Employee Referral'), ('AGENCY', 'Recruitment Agency'), ('DIRECT', 'Direct Inbound')], default='LINKEDIN')
    referred_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidate_referrals')
    match_score_percentage = models.IntegerField(default=85, help_text="AI/Rule match score out of 100")
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal('4.5'))
    recruiter_notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job_requisition', 'candidate')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.candidate.full_name} -> {self.job_requisition.title} [{self.get_stage_display()}]"


class InterviewSchedule(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    round_name = models.CharField(max_length=150, default="Technical Architecture Round 1")
    interview_type = models.CharField(max_length=50, choices=[('VIDEO', 'Video Conference (Google Meet / Zoom)'), ('IN_PERSON', 'On-Site In-Person'), ('PHONE', 'Telephonic Screen')], default='VIDEO')
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    interviewers = models.ManyToManyField(Employee, related_name='scheduled_interviews')
    meeting_link = models.CharField(max_length=255, default="https://meet.google.com/ems-recruitment-room")
    status = models.CharField(max_length=20, choices=[('SCHEDULED', 'Scheduled'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('RESCHEDULED', 'Rescheduled')], default='SCHEDULED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview: {self.application.candidate.full_name} - {self.round_name}"


class InterviewFeedback(models.Model):
    interview = models.ForeignKey(InterviewSchedule, on_delete=models.CASCADE, related_name='feedbacks')
    interviewer = models.ForeignKey(Employee, on_delete=models.CASCADE)
    technical_rating = models.IntegerField(choices=[(1, '1-Poor'), (2, '2-Fair'), (3, '3-Good'), (4, '4-Very Good'), (5, '5-Exceptional')], default=4)
    communication_rating = models.IntegerField(choices=[(1, '1-Poor'), (2, '2-Fair'), (3, '3-Good'), (4, '4-Very Good'), (5, '5-Exceptional')], default=4)
    problem_solving_rating = models.IntegerField(choices=[(1, '1-Poor'), (2, '2-Fair'), (3, '3-Good'), (4, '4-Very Good'), (5, '5-Exceptional')], default=5)
    cultural_fit_rating = models.IntegerField(choices=[(1, '1-Poor'), (2, '2-Fair'), (3, '3-Good'), (4, '4-Very Good'), (5, '5-Exceptional')], default=4)
    recommendation = models.CharField(max_length=30, choices=[('STRONG_HIRE', 'Strong Hire'), ('HIRE', 'Hire'), ('NEUTRAL', 'Neutral / Borderline'), ('NO_HIRE', 'Do Not Hire')], default='HIRE')
    key_strengths = models.TextField()
    areas_for_improvement = models.TextField(blank=True)
    summary_comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('interview', 'interviewer')

    def __str__(self):
        return f"Feedback: {self.interviewer.full_name} on {self.interview.application.candidate.full_name}"


class OfferLetter(models.Model):
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='offer_letter')
    offer_code = models.CharField(max_length=50, unique=True)
    offered_designation = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    offered_ctc_annual = models.DecimalField(max_digits=12, decimal_places=2)
    joining_date = models.DateField()
    probation_months = models.IntegerField(default=6)
    offer_valid_until = models.DateField()
    status = models.CharField(max_length=30, choices=[('DRAFT', 'Draft'), ('APPROVAL_PENDING', 'Pending Internal Signoff'), ('SENT', 'Extended to Candidate'), ('ACCEPTED', 'Accepted & Signed'), ('DECLINED', 'Declined by Candidate'), ('EXPIRED', 'Offer Expired')], default='SENT')
    signed_copy = models.FileField(upload_to='offer_letters/', null=True, blank=True)
    candidate_acceptance_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer: {self.offer_code} -> {self.application.candidate.full_name} ({self.status})"
