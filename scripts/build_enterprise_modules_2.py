import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# 2. APPS / RECRUITMENT (Applicant Tracking System)
# ==============================================================================

write_file("apps/recruitment/__init__.py", """default_app_config = 'apps.recruitment.apps.RecruitmentConfig'""")

write_file("apps/recruitment/apps.py", """
from django.apps import AppConfig

class RecruitmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.recruitment'
    verbose_name = 'Enterprise Recruitment & Applicant Tracking (ATS)'
""")

write_file("apps/recruitment/models.py", """
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
""")

write_file("apps/recruitment/services.py", """
from decimal import Decimal
from django.db.models import Count, Avg
from apps.recruitment.models import JobRequisition, JobApplication, Candidate, InterviewSchedule, OfferLetter

class RecruitmentPipelineService:
    @staticmethod
    def get_pipeline_overview():
        total_open = JobRequisition.objects.filter(status='APPROVED').count()
        total_candidates = Candidate.objects.count()
        total_active_apps = JobApplication.objects.exclude(stage__in=['REJECTED', 'WITHDRAWN', 'HIRED']).count()
        total_offers = OfferLetter.objects.filter(status__in=['SENT', 'ACCEPTED']).count()
        
        stages_breakdown = JobApplication.objects.values('stage').annotate(count=Count('id')).order_by('stage')
        
        return {
            'total_open_positions': total_open,
            'total_candidates': total_candidates,
            'active_applications': total_active_apps,
            'offers_extended': total_offers,
            'stages_breakdown': list(stages_breakdown),
        }

    @staticmethod
    def advance_candidate_stage(application, target_stage, recruiter_user=None):
        application.stage = target_stage
        application.save()
        return application
""")

write_file("apps/recruitment/forms.py", """
from django import forms
from apps.recruitment.models import JobRequisition, Candidate, JobApplication, InterviewSchedule, OfferLetter

class JobRequisitionForm(forms.ModelForm):
    class Meta:
        model = JobRequisition
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'requisition_code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'headcount': forms.NumberInput(attrs={'class': 'form-control'}),
            'hiring_manager': forms.Select(attrs={'class': 'form-select'}),
            'min_experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'work_location': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'justification': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control'}),
            'target_hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'current_company': forms.TextInput(attrs={'class': 'form-control'}),
            'current_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'total_experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_ctc': forms.NumberInput(attrs={'class': 'form-control'}),
            'expected_ctc': forms.NumberInput(attrs={'class': 'form-control'}),
            'notice_period_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_location': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
            'skills_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
""")

write_file("apps/recruitment/views.py", """
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.recruitment.models import JobRequisition, Candidate, JobApplication, InterviewSchedule, OfferLetter
from apps.recruitment.forms import JobRequisitionForm, CandidateForm
from apps.recruitment.services import RecruitmentPipelineService

@login_required
def recruitment_dashboard(request):
    overview = RecruitmentPipelineService.get_pipeline_overview()
    open_requisitions = JobRequisition.objects.filter(status='APPROVED')[:8]
    recent_applications = JobApplication.objects.select_related('candidate', 'job_requisition').order_by('-applied_at')[:10]
    upcoming_interviews = InterviewSchedule.objects.filter(status='SCHEDULED').select_related('application__candidate').order_by('scheduled_start')[:6]
    
    context = {
        'overview': overview,
        'open_requisitions': open_requisitions,
        'recent_applications': recent_applications,
        'upcoming_interviews': upcoming_interviews,
    }
    return render(request, 'recruitment/dashboard.html', context)

@login_required
def requisition_list(request):
    requisitions = JobRequisition.objects.select_related('department', 'hiring_manager')
    return render(request, 'recruitment/requisition_list.html', {'requisitions': requisitions})

@login_required
def requisition_create(request):
    if request.method == 'POST':
        form = JobRequisitionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job requisition created successfully.")
            return redirect('recruitment:requisition_list')
    else:
        form = JobRequisitionForm()
    return render(request, 'recruitment/requisition_form.html', {'form': form, 'title': 'Create Job Requisition'})

@login_required
def candidate_pipeline(request):
    applications = JobApplication.objects.select_related('candidate', 'job_requisition', 'job_requisition__department')
    stages = ['APPLIED', 'SCREENING', 'TECH_INTERVIEW', 'MANAGERIAL', 'HR_ROUND', 'OFFER_EXTENDED', 'HIRED']
    
    pipeline_by_stage = {stage: [] for stage in stages}
    for app in applications:
        if app.stage in pipeline_by_stage:
            pipeline_by_stage[app.stage].append(app)

    return render(request, 'recruitment/pipeline_kanban.html', {'pipeline_by_stage': pipeline_by_stage})

@login_required
def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'recruitment/candidate_list.html', {'candidates': candidates})

@login_required
def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    applications = candidate.applications.select_related('job_requisition')
    return render(request, 'recruitment/candidate_detail.html', {'candidate': candidate, 'applications': applications})

@login_required
def offer_list(request):
    offers = OfferLetter.objects.select_related('application__candidate', 'department')
    return render(request, 'recruitment/offer_list.html', {'offers': offers})
""")

write_file("apps/recruitment/urls.py", """
from django.urls import path
from apps.recruitment import views

app_name = 'recruitment'

urlpatterns = [
    path('', views.recruitment_dashboard, name='dashboard'),
    path('requisitions/', views.requisition_list, name='requisition_list'),
    path('requisitions/create/', views.requisition_create, name='requisition_create'),
    path('pipeline/', views.candidate_pipeline, name='pipeline'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('offers/', views.offer_list, name='offer_list'),
]
""")

write_file("apps/recruitment/admin.py", """
from django.contrib import admin
from apps.recruitment.models import JobRequisition, JobPosting, Candidate, JobApplication, InterviewSchedule, InterviewFeedback, OfferLetter

@admin.register(JobRequisition)
class JobRequisitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'requisition_code', 'department', 'headcount', 'priority', 'status')
    search_fields = ('title', 'requisition_code')
    list_filter = ('status', 'priority', 'department')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'current_company', 'total_experience_years')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job_requisition', 'stage', 'match_score_percentage', 'applied_at')
    list_filter = ('stage', 'source')

@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):
    list_display = ('round_name', 'application', 'interview_type', 'scheduled_start', 'status')

@admin.register(OfferLetter)
class OfferLetterAdmin(admin.ModelAdmin):
    list_display = ('offer_code', 'application', 'offered_ctc_annual', 'joining_date', 'status')
""")

print("Finished Recruitment (ATS) module generation.")
