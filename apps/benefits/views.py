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
