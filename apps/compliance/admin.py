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
