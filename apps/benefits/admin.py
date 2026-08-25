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
