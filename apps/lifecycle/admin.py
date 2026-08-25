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
