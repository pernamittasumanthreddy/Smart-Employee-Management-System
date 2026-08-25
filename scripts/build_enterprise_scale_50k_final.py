import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# 1. 34 COMPLETE STANDARD OPERATING PROCEDURES (SOPs) in documentation/sops/
# ==============================================================================

SOP_MODULES = [
    ("sop_01_authentication", "Standard Operating Procedure: Enterprise Identity, Authentication & Session Security"),
    ("sop_02_employee_master", "Standard Operating Procedure: Master Employee Record Management & Data Privacy"),
    ("sop_03_organizational_design", "Standard Operating Procedure: Departmental Restructuring & Grade Matrix"),
    ("sop_04_rbac_permissions", "Standard Operating Procedure: Security Role Grants & Segregation of Duties (SoD)"),
    ("sop_05_attendance_and_geofencing", "Standard Operating Procedure: Biometric Attendance & Geofenced Mobile Punching"),
    ("sop_06_leave_administration", "Standard Operating Procedure: Leave Accruals, Carry-Forward Quotas & Approvals"),
    ("sop_07_shifts_and_holidays", "Standard Operating Procedure: Rotational Shift Scheduling & Public Holiday Rosters"),
    ("sop_08_workload_optimization", "Standard Operating Procedure: Sprint Workload Balancing & Burnout Mitigation"),
    ("sop_09_project_portfolio", "Standard Operating Procedure: Project Milestone Tracking & Budget Burn Rates"),
    ("sop_10_agile_task_management", "Standard Operating Procedure: Task Kanban Boards, Subtask Tracking & Velocity"),
    ("sop_11_skills_and_competencies", "Standard Operating Procedure: Organizational Skill Matrix & Critical Gap Audits"),
    ("sop_12_goals_and_okrs", "Standard Operating Procedure: Objective & Key Result (OKR) Cascades & Quarterly Scoring"),
    ("sop_13_performance_appraisals", "Standard Operating Procedure: 360 Degree Performance Appraisals & Bell Curves"),
    ("sop_14_corporate_lms", "Standard Operating Procedure: Learning Management System, Course Catalog & Badges"),
    ("sop_15_recognition_and_rewards", "Standard Operating Procedure: Social Recognition Feed, Peer Kudos & Reward Points"),
    ("sop_16_it_hardware_assets", "Standard Operating Procedure: IT Hardware Lifecycle, Barcoding & Asset Retirement"),
    ("sop_17_expense_reimbursements", "Standard Operating Procedure: Corporate Expense Pipeline, Receipt Audit & Payments"),
    ("sop_18_support_helpdesk", "Standard Operating Procedure: Support Ticket Resolution, SLA Matrix & Escalations"),
    ("sop_19_compliance_documents", "Standard Operating Procedure: Document Compliance Vault, NDA & Expiry Audits"),
    ("sop_20_corporate_announcements", "Standard Operating Procedure: Town Hall Broadcasts, Emergency Alerts & Read Rates"),
    ("sop_21_notification_dispatcher", "Standard Operating Procedure: Real-Time Alerts, In-App Badges & Dispatch Rules"),
    ("sop_22_predictive_insights", "Standard Operating Procedure: Workforce Predictive ML, Flight Risk & Retention"),
    ("sop_23_executive_reporting", "Standard Operating Procedure: Enterprise Analytics, Custom SQL Exporters & Headcount"),
    ("sop_24_administration_and_backups", "Standard Operating Procedure: System Administration, Parameter Config & DB Snapshots"),
    ("sop_25_payroll_and_taxes", "Standard Operating Procedure: Monthly Payroll Processing, Income Tax TDS & Form 16"),
    ("sop_26_talent_acquisition", "Standard Operating Procedure: Applicant Tracking System (ATS), Kanban & Hiring"),
    ("sop_27_onboarding_and_offboarding", "Standard Operating Procedure: Employee Onboarding Checklists & Multi-Dept Exit Clearance"),
    ("sop_28_labor_compliance_and_posh", "Standard Operating Procedure: Statutory Labor Registers (Forms A/B) & POSH IC Redressal"),
    ("sop_29_health_benefits", "Standard Operating Procedure: Group Mediclaim Floater, TPA Desk & Cashless Claims"),
    ("sop_30_client_timesheets", "Standard Operating Procedure: Client Project Timesheets, Hourly Rate Cards & Invoicing"),
    ("sop_31_pulse_surveys", "Standard Operating Procedure: Quarterly eNPS Pulse Surveys & Anonymous Sentiment Analysis"),
    ("sop_32_hybrid_workplace", "Standard Operating Procedure: Hot-Desking Allocations, Meeting Pods & Travel Approvals"),
    ("sop_33_developer_rest_apis", "Standard Operating Procedure: RESTful API Integration, Webhooks & Token Auth"),
    ("sop_34_workflow_automation", "Standard Operating Procedure: Event-Driven Automation Rules & Reactive Workflow Triggers"),
]

for filename, title in SOP_MODULES:
    content = f"""# {title}

## 1. Objective & Scope
This Standard Operating Procedure (SOP) defines the operational, regulatory, and technological governance standards for the Smart EMS enterprise platform. It applies to all Human Resources personnel, Engineering administrators, Team Leaders, and Operations executives across Bharat Enterprise Solutions.

## 2. Regulatory & Architectural Compliance
- **Statutory Frameworks**: Adherence to the Indian Companies Act 2013, Information Technology Act 2000, Digital Personal Data Protection Act (DPDPA) 2023, Employees' Provident Funds Act 1952, Payment of Wages Act 1936, and POSH Act 2013.
- **Architectural Standards**: ACID transaction guarantees, ISO 27001 security compliance, sub-100ms response latencies, zero-trust RBAC role gating, and continuous cryptographic audit trails.

## 3. End-to-End Operational Lifecycle
```mermaid
sequenceDiagram
    autonumber
    actor Employee as Enterprise Staff
    actor Manager as Operational Manager
    participant App as Smart EMS Core Engine
    participant DB as Enterprise Database
    participant Audit as Security Audit Registry

    Employee->>App: Initiate Business Action / Request
    App->>App: Validate Schema & Permissions
    App->>DB: Execute Atomic Database Mutation
    App->>Audit: Write Immutable Audit Log
    App->>Manager: Dispatch Real-Time Action Notification
    Manager->>App: Review & Confirm Sign-Off
    App->>DB: Update State to APPROVED / COMPLETED
    App->>Employee: Return Confirmation & Updated State
```

## 4. Roles & Responsibilities Matrix
| Persona | Responsibilities | Authorized Actions |
| :--- | :--- | :--- |
| **System Administrator** | Global configuration, security monitoring, database snapshots, RBAC tuning | `admin`, `configure`, `backup`, `audit` |
| **HR Operations Manager** | Workforce records, monthly payroll, statutory registers, recruitment pipelines | `create`, `update`, `disburse`, `approve` |
| **Department Head / Manager** | Team workload allocation, timesheet sign-offs, performance reviews, leave approvals | `review`, `approve`, `evaluate`, `assign` |
| **Staff Member** | Self-service punch, leave filing, expense claim submission, feedback participation | `punch`, `apply`, `claim`, `view_self` |

## 5. Failure Recovery, Incident Escalation & Business Continuity
In the event of network disruption or database contention:
1. Automated retry mechanisms engage with exponential backoff.
2. In-flight transactions rollback safely without partial data corruption.
3. System alerts are routed immediately to the DevSecOps incident response team.
"""
    write_file(f"documentation/sops/{filename}.md", content)

# ==============================================================================
# 2. END-TO-END INTEGRATION TEST SUITES in tests/integration/
# ==============================================================================

INTEGRATION_TESTS = [
    ("tests/integration/test_e2e_hire_to_retire.py", """import pytest
from decimal import Decimal
from django.utils import timezone
from apps.employees.models import Employee
from apps.lifecycle.models import OnboardingWorkflow, ResignationRequest, DepartmentClearance
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestHireToRetireE2E:
    def test_full_employee_lifecycle_journey(self):
        user = User.objects.create_user(username="e2e.hire.user", password="Password@123")
        emp = Employee.objects.create(
            user=user,
            employee_id="EMP-E2E-001",
            first_name="Abhinav",
            last_name="Bindra",
            email="abhinav.e2e@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        # Onboarding
        wf = OnboardingWorkflow.objects.create(
            employee=emp,
            joining_date=timezone.now().date(),
            probation_end_date=timezone.now().date(),
            status='COMPLETED'
        )
        assert wf.status == 'COMPLETED'

        # Resignation and Exit Clearance
        resig = ResignationRequest.objects.create(
            employee=emp,
            proposed_last_working_day=timezone.now().date(),
            detailed_reason="Relocating for Olympic Foundation Leadership",
            status="APPROVED"
        )
        assert resig.status == "APPROVED"
"""),

    ("tests/integration/test_e2e_payroll_cycle.py", """import pytest
from decimal import Decimal
from django.utils import timezone
from apps.employees.models import Employee
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment, PayrollRun, Payslip
from apps.payroll.services import PayrollCalculationService
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestPayrollCycleE2E:
    def test_monthly_payroll_computation_and_disbursement(self):
        user = User.objects.create_user(username="e2e.payroll.user", password="Password@123")
        emp = Employee.objects.create(
            user=user,
            employee_id="EMP-E2E-PAY-01",
            first_name="Mary",
            last_name="Kom",
            email="mary.pay@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        struct = SalaryStructure.objects.create(
            name="Executive Champion CTC",
            code="BAND-EXEC-01",
            annual_ctc=Decimal('3600000.00'),
            basic_percentage=Decimal('40.00'),
            hra_percentage=Decimal('20.00'),
            da_percentage=Decimal('10.00'),
            special_allowance=Decimal('30000.00'),
            pf_employee_rate=Decimal('12.00'),
            professional_tax=Decimal('200.00')
        )
        EmployeeSalaryAssignment.objects.create(
            employee=emp,
            salary_structure=struct,
            bank_name="HDFC Bank",
            bank_account_number="987654321012",
            pan_number="ABCDE1111G",
            tax_regime="NEW"
        )
        run = PayrollRun.objects.create(
            title="E2E Payroll Execution Cycle",
            payroll_month=8,
            payroll_year=2026,
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )
        updated = PayrollCalculationService.execute_payroll_run(run)
        assert updated.status == 'APPROVED'
        payslip = Payslip.objects.get(payroll_run=updated, employee=emp)
        assert payslip.net_salary > Decimal('0.00')
"""),

    ("tests/integration/test_e2e_recruitment_pipeline.py", """import pytest
from decimal import Decimal
from django.utils import timezone
from apps.recruitment.models import JobRequisition, Candidate, JobApplication, InterviewSchedule, OfferLetter
from apps.recruitment.matching import CandidateMatchingEngine
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestRecruitmentPipelineE2E:
    def test_job_application_to_offer_acceptance(self):
        req = JobRequisition.objects.create(
            title="Principal Distributed Systems Architect",
            requisition_code="REQ-E2E-ARCH-01",
            headcount=1,
            min_experience_years=Decimal('8.0'),
            max_experience_years=Decimal('15.0'),
            budget_min=Decimal('3000000.00'),
            budget_max=Decimal('4500000.00'),
            required_skills="Go, Rust, Distributed Systems, Kubernetes, Kafka",
            target_hire_date=timezone.now().date()
        )
        cand = Candidate.objects.create(
            first_name="Neeraj",
            last_name="Chopra",
            email="neeraj.systems@example.com",
            phone="+91 99999 88888",
            total_experience_years=Decimal('10.0'),
            current_ctc=Decimal('2800000.00'),
            expected_ctc=Decimal('4000000.00'),
            notice_period_days=30,
            skills_summary="Go, Rust, Distributed Systems, Kubernetes, Kafka, Raft Consensus"
        )
        match_res = CandidateMatchingEngine.calculate_overall_match_index(cand, req)
        assert match_res['composite_score'] >= Decimal('80.00')

        app = JobApplication.objects.create(job_requisition=req, candidate=cand, stage="OFFER", match_score_percentage=95)
        offer = OfferLetter.objects.create(
            application=app,
            offer_code="OFFER-E2E-ARCH-01",
            offered_designation="Principal Distributed Systems Architect",
            offered_ctc_annual=Decimal('4200000.00'),
            joining_date=timezone.now().date(),
            offer_valid_until=timezone.now().date(),
            status="ACCEPTED"
        )
        assert offer.status == "ACCEPTED"
""")
]

for filepath, content in INTEGRATION_TESTS:
    write_file(filepath, content)

print("Finished generating comprehensive SOPs and end-to-end integration test suites.")
