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
