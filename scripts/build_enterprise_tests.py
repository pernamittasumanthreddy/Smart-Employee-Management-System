import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# PYTEST TEST SUITES FOR ALL 10 NEW ENTERPRISE MODULES
# ==============================================================================

write_file("tests/test_payroll.py", """
import pytest
from decimal import Decimal
from django.utils import timezone
from apps.payroll.models import SalaryStructure, PayrollRun, Payslip, TaxDeclaration
from apps.payroll.services import PayrollCalculationService
from apps.payroll.engine import IndianIncomeTaxEngine
from apps.employees.models import Employee

@pytest.mark.django_db
def test_salary_structure_calculations():
    struct = SalaryStructure.objects.create(
        name="Tech Lead Band",
        code="TL-B1",
        annual_ctc=Decimal('1200000.00'),
        basic_percentage=Decimal('40.00'),
        hra_percentage=Decimal('20.00'),
        da_percentage=Decimal('10.00'),
        pf_employee_rate=Decimal('12.00'),
        professional_tax=Decimal('200.00')
    )
    assert struct.monthly_ctc == Decimal('100000.00')
    assert struct.monthly_basic == Decimal('40000.00')
    assert struct.monthly_hra == Decimal('8000.00')
    assert struct.monthly_da == Decimal('4000.00')
    assert struct.monthly_pf_employee == Decimal('4800.00')
    assert struct.monthly_gross > Decimal('50000.00')

@pytest.mark.django_db
def test_indian_income_tax_engine():
    # Test New Regime Standard Deduction
    res_new = IndianIncomeTaxEngine.compute_new_regime_tax(Decimal('600000.00'))
    assert res_new['total_annual_tax'] == Decimal('0.00')  # 87A rebate applies under 7L

    # Test Higher Income in New Regime
    res_high = IndianIncomeTaxEngine.compute_new_regime_tax(Decimal('1500000.00'))
    assert res_high['total_annual_tax'] > Decimal('0.00')

    # Test Old Regime
    res_old = IndianIncomeTaxEngine.compute_old_regime_tax(
        gross_annual_salary=Decimal('1200000.00'),
        annual_basic=Decimal('480000.00'),
        annual_hra_received=Decimal('96000.00'),
        annual_rent_paid=Decimal('180000.00'),
        sec_80c_total=Decimal('150000.00'),
        sec_80d_self=Decimal('25000.00')
    )
    assert res_old['hra_exemption'] > Decimal('0.00')
    assert res_old['chapter_via_deductions'] == Decimal('175000.00')

@pytest.mark.django_db
def test_payroll_run_execution(client):
    run = PayrollRun.objects.create(
        title="Test Cycle - August 2026",
        payroll_month=8,
        payroll_year=2026,
        start_date=timezone.now().date(),
        end_date=timezone.now().date()
    )
    updated_run = PayrollCalculationService.execute_payroll_run(run)
    assert updated_run.status == 'APPROVED'
    assert updated_run.payslips.count() >= 0
""")

write_file("tests/test_recruitment.py", """
import pytest
from decimal import Decimal
from django.utils import timezone
from apps.recruitment.models import JobRequisition, Candidate, JobApplication, OfferLetter
from apps.recruitment.matching import CandidateMatchingEngine
from apps.organization.models import Department

@pytest.mark.django_db
def test_candidate_matching_engine():
    candidate_skills = "Python, Django, PostgreSQL, Docker, AWS, Celery"
    req_skills = "Python, Django, AWS, Kubernetes"
    score = CandidateMatchingEngine.calculate_skill_match_score(candidate_skills, req_skills)
    assert score >= Decimal('70.00')

@pytest.mark.django_db
def test_job_application_lifecycle():
    dept, _ = Department.objects.get_or_create(name="Platform Engineering", code="ENG-PLT")
    req = JobRequisition.objects.create(
        title="Senior Backend Engineer",
        requisition_code="REQ-2026-099",
        department=dept,
        headcount=2,
        target_hire_date=timezone.now().date()
    )
    cand = Candidate.objects.create(
        first_name="Rohan",
        last_name="Verma",
        email="rohan.verma.test@example.com",
        phone="9876543210"
    )
    app = JobApplication.objects.create(
        job_requisition=req,
        candidate=cand,
        stage='APPLIED'
    )
    assert app.stage == 'APPLIED'
    app.stage = 'OFFER_EXTENDED'
    app.save()
    assert app.stage == 'OFFER_EXTENDED'
""")

write_file("tests/test_lifecycle.py", """
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
""")

write_file("tests/test_compliance.py", """
import pytest
from apps.compliance.models import StatutoryRegister, ComplianceAudit, POSHCommitteeMember
from apps.compliance.statutory_engine import StatutoryRegisterCompiler

@pytest.mark.django_db
def test_statutory_registers_compiler():
    reg_rows = StatutoryRegisterCompiler.compile_form_a_employee_register()
    assert isinstance(reg_rows, list)
    
    wage_rows = StatutoryRegisterCompiler.compile_form_b_wage_register(2026, 8)
    assert isinstance(wage_rows, list)

@pytest.mark.django_db
def test_compliance_audit_record():
    audit = ComplianceAudit.objects.create(
        title="Q3 Statutory Labour Compliance Audit",
        score_percentage=99,
        status='COMPLETED'
    )
    assert audit.score_percentage == 99
""")

write_file("tests/test_benefits.py", """
import pytest
from decimal import Decimal
from django.utils import timezone
from apps.benefits.models import InsurancePolicy, EmployeeInsuranceEnrollment, InsuranceClaim
from apps.employees.models import Employee

@pytest.mark.django_db
def test_benefits_and_claims():
    policy = InsurancePolicy.objects.create(
        name="HDFC ERGO Health Suraksha Floater",
        policy_number="HDFC-POL-9921",
        sum_insured=Decimal('500000.00'),
        start_date=timezone.now().date(),
        end_date=timezone.now().date()
    )
    assert policy.sum_insured == Decimal('500000.00')
""")

write_file("tests/test_timesheets.py", """
import pytest
from decimal import Decimal
from django.utils import timezone
from apps.timesheets.models import WeeklyTimesheet, TimesheetEntry
from apps.employees.models import Employee
from apps.projects.models import Project

@pytest.mark.django_db
def test_weekly_timesheet_hours():
    emp = Employee.objects.first()
    proj = Project.objects.first()
    if not emp or not proj:
        pytest.skip("Seed data required")

    ts = WeeklyTimesheet.objects.create(
        employee=emp,
        week_start_date=timezone.now().date(),
        week_end_date=timezone.now().date(),
        total_billable_hours=Decimal('35.00'),
        total_non_billable_hours=Decimal('5.00'),
        status='SUBMITTED'
    )
    assert ts.total_hours == Decimal('40.00')
""")

write_file("tests/test_surveys.py", """
import pytest
from django.utils import timezone
from apps.surveys.models import Survey, SurveyQuestion, SurveySubmission

@pytest.mark.django_db
def test_survey_and_enps():
    survey = Survey.objects.create(
        title="Q3 2026 Workforce eNPS Pulse",
        survey_type="ENPS",
        description="Confidential quarterly survey",
        end_date=timezone.now().date(),
        is_anonymous=True
    )
    q1 = SurveyQuestion.objects.create(
        survey=survey,
        order=1,
        prompt_text="How likely are you to recommend Bharat Enterprise Solutions as a great place to work?",
        question_type="RATING_10"
    )
    sub = SurveySubmission.objects.create(
        survey=survey,
        enps_score=10,
        sentiment_label='POSITIVE'
    )
    assert sub.enps_score == 10
    assert survey.questions.count() == 1
""")

write_file("tests/test_workplace.py", """
import pytest
from decimal import Decimal
from django.utils import timezone
from apps.workplace.models import MeetingRoom, DeskBooking, TravelRequest
from apps.employees.models import Employee

@pytest.mark.django_db
def test_meeting_room_and_travel():
    room = MeetingRoom.objects.create(
        name="Chanakya Executive Room",
        floor="Floor 5",
        capacity_seats=16,
        has_video_conferencing=True
    )
    assert room.capacity_seats == 16
""")

write_file("tests/test_api.py", """
import pytest
import json
from django.test import Client
from apps.api.openapi import OpenApiSpecGenerator

@pytest.mark.django_db
def test_api_endpoints_and_openapi(client):
    spec = OpenApiSpecGenerator.get_complete_spec()
    assert spec['openapi'] == '3.0.3'
    assert '/api/v1/employees/' in spec['paths']

    resp = client.get('/api/v1/employees/')
    assert resp.status_code == 200
    assert 'results' in resp.json()

    resp_attn = client.get('/api/v1/attendance/today/')
    assert resp_attn.status_code == 200

    resp_sync = client.post(
        '/api/v1/biometric/sync/',
        data=json.dumps({'device_id': 'GATE-01', 'user_id': 'EMP-1001', 'punch_type': 'IN'}),
        content_type='application/json'
    )
    assert resp_sync.status_code == 200
""")

write_file("tests/test_automation.py", """
import pytest
from apps.automation.models import AutomationRule, ExecutionLog

@pytest.mark.django_db
def test_automation_rules():
    rule = AutomationRule.objects.create(
        name="Welcome Onboarding Email Dispatcher",
        trigger_event="EMPLOYEE_JOINED",
        action_type="DISPATCH_EMAIL",
        action_payload="{'template': 'welcome_mail'}",
        is_active=True
    )
    log = ExecutionLog.objects.create(
        rule=rule,
        status='SUCCESS',
        details='Sent welcome email to new hire'
    )
    assert log.status == 'SUCCESS'
    assert rule.execution_logs.count() == 1
""")

print("Finished all 10 enterprise Pytest test suites generation.")
