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
