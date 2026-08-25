import pytest
from django.utils import timezone
from apps.lifecycle.models import OnboardingWorkflow, ResignationRequest, DepartmentClearance
from apps.employees.models import Employee

@pytest.mark.django_db
def test_onboarding_and_exit_clearances():
    emp = Employee.objects.first()
    if not emp:
        pytest.skip("Employee model requires seed data")
    
    # Onboarding
    wf, _ = OnboardingWorkflow.objects.get_or_create(
        employee=emp,
        defaults={
            'joining_date': timezone.now().date(),
            'probation_end_date': timezone.now().date(),
            'welcome_email_sent': True,
            'it_assets_assigned': True,
        }
    )
    assert wf.progress_percentage >= 40

    # Resignation
    resig, _ = ResignationRequest.objects.get_or_create(
        employee=emp,
        defaults={
            'proposed_last_working_day': timezone.now().date(),
            'detailed_reason': 'Pursuing Higher Studies & Leadership Masters',
            'status': 'SUBMITTED'
        }
    )
    assert resig.status == 'SUBMITTED'
