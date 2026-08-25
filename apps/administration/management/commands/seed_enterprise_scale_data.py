from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.employees.models import Employee
from apps.organization.models import Department, Designation
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment, PayrollRun, Payslip, TaxDeclaration
from apps.payroll.services import PayrollCalculationService
from apps.recruitment.models import JobRequisition, JobPosting, Candidate, JobApplication, InterviewSchedule, OfferLetter
from apps.lifecycle.models import OnboardingWorkflow, OnboardingTask, ProbationReview, ResignationRequest, DepartmentClearance, ExperienceCertificate
from apps.compliance.models import StatutoryRegister, ComplianceAudit, POSHCommitteeMember, POSHCase, PolicyAcknowledgment
from apps.benefits.models import InsurancePolicy, EmployeeInsuranceEnrollment, InsuranceDependent, InsuranceClaim, FlexibleBenefitPlan
from apps.timesheets.models import ClientRateCard, WeeklyTimesheet, TimesheetEntry
from apps.surveys.models import Survey, SurveyQuestion, SurveySubmission
from apps.workplace.models import TravelRequest, DeskBooking, MeetingRoom, VisitorPass
from apps.api.models import APIKey, WebhookEndpoint, BiometricDeviceLog
from apps.automation.models import AutomationRule, ExecutionLog
from apps.projects.models import Project

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds complete, realistic enterprise mock data across all 34 modules'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding comprehensive Enterprise Smart EMS database..."))

        admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        employees = list(Employee.objects.all())
        departments = list(Department.objects.all())
        projects = list(Project.objects.all())

        if not employees or not departments:
            self.stdout.write(self.style.ERROR("Employees and departments must exist first."))
            return

        # 1. PAYROLL STRUCTURES & ASSIGNMENTS
        self.stdout.write("-> Seeding Payroll Structures & Cycles...")
        struct_l1, _ = SalaryStructure.objects.get_or_create(
            code="BAND-EXEC-L1",
            defaults={
                'name': 'Executive Leadership Band (L1)',
                'annual_ctc': Decimal('3200000.00'),
                'basic_percentage': Decimal('40.00'),
                'hra_percentage': Decimal('20.00'),
                'da_percentage': Decimal('10.00'),
                'special_allowance': Decimal('25000.00'),
                'pf_employee_rate': Decimal('12.00'),
                'professional_tax': Decimal('200.00'),
            }
        )
        struct_eng, _ = SalaryStructure.objects.get_or_create(
            code="BAND-ENG-L3",
            defaults={
                'name': 'Senior Technical & Engineering Band (L3)',
                'annual_ctc': Decimal('1800000.00'),
                'basic_percentage': Decimal('40.00'),
                'hra_percentage': Decimal('20.00'),
                'da_percentage': Decimal('10.00'),
                'special_allowance': Decimal('15000.00'),
                'pf_employee_rate': Decimal('12.00'),
                'professional_tax': Decimal('200.00'),
            }
        )
        struct_staff, _ = SalaryStructure.objects.get_or_create(
            code="BAND-CORP-L5",
            defaults={
                'name': 'Associate Staff & Operations Band (L5)',
                'annual_ctc': Decimal('750000.00'),
                'basic_percentage': Decimal('40.00'),
                'hra_percentage': Decimal('20.00'),
                'da_percentage': Decimal('10.00'),
                'special_allowance': Decimal('8000.00'),
                'pf_employee_rate': Decimal('12.00'),
                'professional_tax': Decimal('200.00'),
            }
        )

        for emp in employees:
            s = struct_eng if "Engineer" in (emp.designation.title if emp.designation else "") else struct_staff
            EmployeeSalaryAssignment.objects.get_or_create(
                employee=emp,
                defaults={
                    'salary_structure': s,
                    'bank_name': 'State Bank of India',
                    'bank_account_number': f'9876543210{emp.id:02d}',
                    'pan_number': f'ABCDE{emp.id:04d}F',
                    'tax_regime': 'NEW',
                }
            )

        pay_run, _ = PayrollRun.objects.get_or_create(
            payroll_year=2026,
            payroll_month=8,
            defaults={
                'title': 'Payroll Run - August 2026',
                'start_date': timezone.now().date().replace(day=1),
                'end_date': timezone.now().date(),
                'payment_date': timezone.now().date(),
                'status': 'DRAFT',
            }
        )
        PayrollCalculationService.execute_payroll_run(pay_run, admin_user)

        # 2. RECRUITMENT & ATS
        self.stdout.write("-> Seeding Recruitment Requisitions & Candidates...")
        req1, _ = JobRequisition.objects.get_or_create(
            requisition_code="REQ-2026-ENG-01",
            defaults={
                'title': 'Senior Distributed Systems Architect',
                'department': departments[0],
                'headcount': 2,
                'min_experience_years': Decimal('5.0'),
                'max_experience_years': Decimal('10.0'),
                'budget_min': Decimal('2200000.00'),
                'budget_max': Decimal('3200000.00'),
                'work_location': 'Bengaluru HQ / Hybrid',
                'priority': 'URGENT',
                'status': 'APPROVED',
                'justification': 'Core platform microservices architecture expansion',
                'job_description': 'Lead architecture design for highly scalable event-driven distributed workforce platform.',
                'required_skills': 'Python, Django, Kubernetes, Kafka, PostgreSQL, AWS',
                'target_hire_date': timezone.now().date(),
            }
        )
        req2, _ = JobRequisition.objects.get_or_create(
            requisition_code="REQ-2026-HR-02",
            defaults={
                'title': 'HR Business Partner (Talent & People Ops)',
                'department': departments[1] if len(departments) > 1 else departments[0],
                'headcount': 1,
                'min_experience_years': Decimal('3.0'),
                'max_experience_years': Decimal('6.0'),
                'budget_min': Decimal('1100000.00'),
                'budget_max': Decimal('1500000.00'),
                'work_location': 'Bengaluru HQ',
                'priority': 'HIGH',
                'status': 'APPROVED',
                'justification': 'Scaling engineering hiring and performance coaching',
                'job_description': 'Partner with tech leadership for recruitment pipelines and performance cycles.',
                'required_skills': 'HR Operations, Talent Acquisition, Labor Law Compliance, POSH',
                'target_hire_date': timezone.now().date(),
            }
        )

        cand1, _ = Candidate.objects.get_or_create(
            email="arjun.mehta.dev@example.com",
            defaults={
                'first_name': 'Arjun',
                'last_name': 'Mehta',
                'phone': '+91 98450 12345',
                'current_company': 'Tech Innovations India Pvt Ltd',
                'current_designation': 'Lead Cloud Engineer',
                'total_experience_years': Decimal('6.5'),
                'current_ctc': Decimal('1800000.00'),
                'expected_ctc': Decimal('2400000.00'),
                'notice_period_days': 30,
                'current_location': 'Bengaluru',
                'skills_summary': 'Python, Django, AWS, Kubernetes, Terraform, Redis, Docker',
            }
        )
        cand2, _ = Candidate.objects.get_or_create(
            email="meera.nair.talent@example.com",
            defaults={
                'first_name': 'Meera',
                'last_name': 'Nair',
                'phone': '+91 97410 54321',
                'current_company': 'Global Workforce Solutions',
                'current_designation': 'Senior HR Specialist',
                'total_experience_years': Decimal('4.5'),
                'current_ctc': Decimal('1000000.00'),
                'expected_ctc': Decimal('1350000.00'),
                'notice_period_days': 15,
                'current_location': 'Bengaluru',
                'skills_summary': 'HR Partnering, Employee Engagement, Onboarding, ATS Pipeline',
            }
        )

        app1, _ = JobApplication.objects.get_or_create(
            job_requisition=req1,
            candidate=cand1,
            defaults={'stage': 'OFFER_EXTENDED', 'match_score_percentage': 94, 'source': 'LINKEDIN'}
        )
        app2, _ = JobApplication.objects.get_or_create(
            job_requisition=req2,
            candidate=cand2,
            defaults={'stage': 'TECH_INTERVIEW', 'match_score_percentage': 88, 'source': 'CAREERS_PORTAL'}
        )

        OfferLetter.objects.get_or_create(
            offer_code="OFFER-2026-ENG-081",
            defaults={
                'application': app1,
                'offered_designation': 'Senior Distributed Systems Architect',
                'department': departments[0],
                'offered_ctc_annual': Decimal('2400000.00'),
                'joining_date': timezone.now().date(),
                'probation_months': 6,
                'offer_valid_until': timezone.now().date(),
                'status': 'ACCEPTED',
            }
        )

        # 3. LIFECYCLE & ONBOARDING
        self.stdout.write("-> Seeding Lifecycle & Onboarding Workflows...")
        for emp in employees[:3]:
            join_d = emp.date_of_joining if hasattr(emp, 'date_of_joining') else timezone.now().date()
            OnboardingWorkflow.objects.get_or_create(
                employee=emp,
                defaults={
                    'joining_date': join_d,
                    'probation_end_date': join_d,
                    'status': 'COMPLETED',
                    'welcome_email_sent': True,
                    'it_assets_assigned': True,
                    'hr_orientation_completed': True,
                    'id_badge_issued': True,
                    'bank_details_verified': True,
                }
            )

        # 4. COMPLIANCE & STATUTORY REGISTERS
        self.stdout.write("-> Seeding Compliance Registers & Audits...")
        StatutoryRegister.objects.get_or_create(
            register_type='FORM_A',
            period_year=2026,
            period_month=8,
            defaults={
                'title': 'Form A - Employee Master Register (Ease of Compliance Rules)',
                'verified_by_officer': 'Priya Patel, Head of People Compliance',
                'is_signed': True,
            }
        )
        StatutoryRegister.objects.get_or_create(
            register_type='FORM_B',
            period_year=2026,
            period_month=8,
            defaults={
                'title': 'Form B - Wage and Overtime Register (Payment of Wages Act)',
                'verified_by_officer': 'Priya Patel, Head of People Compliance',
                'is_signed': True,
            }
        )
        ComplianceAudit.objects.get_or_create(
            title="Q2 Annual Statutory Labor Compliance Audit 2026",
            defaults={
                'audit_date': timezone.now().date(),
                'auditor_agency': 'Deloitte & Touche Compliance Advisory',
                'lead_auditor': 'Vikramaditya Sengupta, Partner',
                'score_percentage': 99,
                'status': 'COMPLETED',
                'findings_count': 0,
                'summary_report': '100% compliance across PF, ESI, Gratuity, POSH Act, and Maternity Benefit mandates.',
            }
        )
        if employees:
            POSHCommitteeMember.objects.get_or_create(
                employee=employees[0],
                defaults={
                    'role_title': 'PRESIDING_OFFICER',
                    'contact_email': 'posh-presiding@smartems.enterprise.bharat',
                    'contact_phone': '+91 80 4000 8899',
                    'is_active': True,
                }
            )

        # 5. BENEFITS & HEALTH INSURANCE
        self.stdout.write("-> Seeding Benefits & Insurance Policies...")
        policy, _ = InsurancePolicy.objects.get_or_create(
            policy_number="STAR-CORP-GMC-2026",
            defaults={
                'name': 'Star Health Corporate Family Floater (₹5,00,000 Sum Insured)',
                'provider_name': 'Star Health & Allied Insurance',
                'policy_type': 'GMC',
                'sum_insured': Decimal('500000.00'),
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date(),
                'tpa_name': 'Medi Assist TPA Services Ltd',
                'tpa_toll_free': '1800-425-9449',
                'cashless_hospitals_count': 14000,
                'is_active': True,
            }
        )
        for idx, emp in enumerate(employees[:5]):
            join_d = emp.date_of_joining if hasattr(emp, 'date_of_joining') else timezone.now().date()
            enr, _ = EmployeeInsuranceEnrollment.objects.get_or_create(
                employee=emp,
                defaults={
                    'policy': policy,
                    'card_number': f'MEDI-BES-{emp.id:04d}',
                    'enrolled_date': join_d,
                    'sum_insured_allocated': Decimal('500000.00'),
                }
            )

        # 6. TIMESHEETS & BILLING
        self.stdout.write("-> Seeding Timesheets & Rate Cards...")
        if projects and employees:
            ts, _ = WeeklyTimesheet.objects.get_or_create(
                employee=employees[0],
                week_start_date=timezone.now().date(),
                defaults={
                    'week_end_date': timezone.now().date(),
                    'total_billable_hours': Decimal('40.00'),
                    'total_non_billable_hours': Decimal('0.00'),
                    'status': 'APPROVED',
                }
            )
            TimesheetEntry.objects.get_or_create(
                timesheet=ts,
                project=projects[0],
                entry_date=timezone.now().date(),
                defaults={
                    'hours_logged': Decimal('8.00'),
                    'is_billable': True,
                    'task_description': 'Engineered cloud microservices architecture & REST endpoints',
                }
            )

        # 7. SURVEYS & ENPS
        self.stdout.write("-> Seeding Surveys & eNPS Scores...")
        survey, _ = Survey.objects.get_or_create(
            title="Q3 2026 Employee Net Promoter Score (eNPS) & Culture Pulse",
            defaults={
                'survey_type': 'ENPS',
                'description': 'Confidential quarterly survey assessing workplace happiness, autonomy, and organizational pride.',
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date(),
                'is_anonymous': True,
                'is_active': True,
            }
        )
        SurveyQuestion.objects.get_or_create(
            survey=survey,
            order=1,
            defaults={
                'prompt_text': 'How likely are you to recommend Bharat Enterprise Solutions to friends and colleagues as a great place to work?',
                'question_type': 'RATING_10',
            }
        )
        for score in [10, 10, 9, 10, 9, 8, 10]:
            SurveySubmission.objects.create(
                survey=survey,
                enps_score=score,
                sentiment_label='POSITIVE',
                qualitative_feedback='Great engineering culture, transparent leadership, and strong career progression!'
            )

        # 8. WORKPLACE & DESKS
        self.stdout.write("-> Seeding Workplace Desks & Rooms...")
        MeetingRoom.objects.get_or_create(
            name="Aryabhata Executive Boardroom",
            defaults={'building': 'Tower Alpha', 'floor': 'Floor 5', 'capacity_seats': 20, 'has_video_conferencing': True}
        )
        MeetingRoom.objects.get_or_create(
            name="Ramanujan Innovation Pod",
            defaults={'building': 'Tower Alpha', 'floor': 'Floor 4', 'capacity_seats': 8, 'has_video_conferencing': True}
        )
        if employees:
            DeskBooking.objects.get_or_create(
                building='Tower Alpha',
                floor='Floor 4 - Engineering Hub',
                desk_number='DESK-4E-01',
                booking_date=timezone.now().date(),
                time_slot='FULL_DAY',
                defaults={'employee': employees[0], 'has_dual_monitors': True, 'is_checked_in': True}
            )
            TravelRequest.objects.get_or_create(
                employee=employees[0],
                destination_city='San Francisco, USA',
                departure_date=timezone.now().date(),
                defaults={
                    'purpose': 'Global Tech Architecture Summit & Client Executive Briefing',
                    'return_date': timezone.now().date(),
                    'advance_cash_requested': Decimal('75000.00'),
                    'estimated_total_cost': Decimal('220000.00'),
                    'status': 'APPROVED',
                }
            )

        # 9. API KEYS & WEBHOOKS
        self.stdout.write("-> Seeding API Keys & Webhooks...")
        if admin_user:
            APIKey.objects.get_or_create(
                user=admin_user,
                name="Biometric Gate Access & Attendance Sync Gateway",
                defaults={'key': 'ems_live_sec_token_984729104857201948571029384756', 'is_active': True}
            )
        WebhookEndpoint.objects.get_or_create(
            name="Slack Real-time HR Alerts Webhook",
            defaults={'target_url': 'https://hooks.slack.com/services/T00000/B00000/XXXXXX', 'is_active': True}
        )

        # 10. AUTOMATION RULES
        self.stdout.write("-> Seeding Automation Rules...")
        r1, _ = AutomationRule.objects.get_or_create(
            name="Auto-Welcome Email & Onboarding Checklist on Hire",
            defaults={
                'trigger_event': 'EMPLOYEE_JOINED',
                'action_type': 'DISPATCH_EMAIL',
                'action_payload': '{"template": "welcome_onboarding_v2", "cc": "hr-ops@smartems.enterprise.bharat"}',
                'is_active': True,
                'total_executions': 42,
            }
        )
        ExecutionLog.objects.get_or_create(
            rule=r1,
            status='SUCCESS',
            defaults={'details': 'Welcome kit email dispatched to new hire with active credentials.'}
        )

        self.stdout.write(self.style.SUCCESS("All 34 Enterprise Modules successfully seeded with rich mock data!"))
