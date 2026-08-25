from datetime import date
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.employees.models import Employee
from apps.lifecycle.models import (
    DepartmentClearance,
    ExperienceCertificate,
    OnboardingTask,
    OnboardingWorkflow,
    ProbationReview,
    ResignationRequest,
)


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


@login_required
def letters_hub_view(request):
    """
    Self-Service HR Letters & Official Certificates Studio:
    Allows employees to request and 1-click generate letters.
    Allows HR/Admin to generate letters for any employee.
    """
    user = request.user
    is_privileged = user.is_superuser or getattr(user, 'role', '') in ['ADMIN', 'HR', 'MANAGER']
    
    employees_list = None
    if is_privileged:
        employees_list = Employee.objects.filter(employment_status='ACTIVE').select_related('department', 'designation')

    current_emp = getattr(user, 'employee_profile', None)
    if not current_emp and employees_list:
        current_emp = employees_list.first()

    return render(request, 'lifecycle/letters_hub.html', {
        'current_emp': current_emp,
        'employees_list': employees_list,
        'is_privileged': is_privileged,
    })


@login_required
def letter_generator_view(request):
    """
    Renders the official, printable company letter with header, watermark,
    reference ID, and authorized digital stamp.
    """
    user = request.user
    is_privileged = user.is_superuser or getattr(user, 'role', '') in ['ADMIN', 'HR', 'MANAGER']
    
    emp_id = request.GET.get('employee_id')
    letter_type = request.GET.get('type', 'employment_verification')
    addressed_to = request.GET.get('addressed_to', 'To Whom It May Concern').strip() or 'To Whom It May Concern'
    purpose = request.GET.get('purpose', '').strip()

    if is_privileged and emp_id:
        target_employee = get_object_or_404(Employee, id=emp_id)
    else:
        target_employee = getattr(user, 'employee_profile', None)
        if not target_employee:
            target_employee = Employee.objects.filter(employment_status='ACTIVE').first()

    if not target_employee:
        messages.error(request, "Employee record not found.")
        return redirect('lifecycle:letters_hub')

    # Generate Unique Reference Number
    ref_code = f"BES/HR/{timezone.now().year}/{target_employee.employee_id}/{letter_type[:3].upper()}-{str(uuid.uuid4())[:6].upper()}"
    issue_date = timezone.now().date()

    # Determine letter template titles and metadata
    letter_meta = {
        'employment_verification': {
            'title': 'CERTIFICATE OF EMPLOYMENT VERIFICATION',
            'subject': f'Confirmation of Employment for {target_employee.full_name}',
        },
        'salary_certificate': {
            'title': 'SALARY & REMUNERATION CERTIFICATE',
            'subject': f'Proof of Remuneration & Income for {target_employee.full_name}',
        },
        'bonafide_visa': {
            'title': 'BONAFIDE & VISA TRAVEL SUPPORT LETTER',
            'subject': f'Official Bonafide Travel & Employment Endorsement for {target_employee.full_name}',
        },
        'experience_letter': {
            'title': 'EXPERIENCE & SERVICE RECORD CERTIFICATE',
            'subject': f'Service & Experience Record for {target_employee.full_name}',
        },
        'noc_letter': {
            'title': 'NO OBJECTION CERTIFICATE (NOC)',
            'subject': f'No Objection Letter for {target_employee.full_name}',
        },
    }

    selected_meta = letter_meta.get(letter_type, letter_meta['employment_verification'])

    # Optional compensation calculation
    monthly_ctc = 85000.00
    annual_ctc = monthly_ctc * 12.0

    return render(request, 'lifecycle/official_letter_preview.html', {
        'employee': target_employee,
        'letter_type': letter_type,
        'letter_title': selected_meta['title'],
        'subject': selected_meta['subject'],
        'ref_code': ref_code,
        'issue_date': issue_date,
        'addressed_to': addressed_to,
        'purpose': purpose,
        'monthly_ctc': monthly_ctc,
        'annual_ctc': annual_ctc,
    })
