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
