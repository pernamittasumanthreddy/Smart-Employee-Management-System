import random
from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.administration.models import (
    AuditAction,
    AuditLog,
    BackupConfiguration,
    SystemSetting,
)
from apps.announcements.models import (
    Announcement,
    AnnouncementCategory,
    CompanyEvent,
    EventRegistration,
)
from apps.assets.models import Asset, AssetCategory, AssetStatus
from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.authentication.models import User
from apps.documents.models import DocumentCategory, EmployeeDocument
from apps.employees.models import (
    Employee,
    EmployeeBankDetail,
    EmployeeEducation,
    EmployeeExperience,
    EmploymentStatus,
    EmploymentType,
    Gender,
)
from apps.expenses.models import ExpenseCategory, ExpenseClaim, ExpenseStatus
from apps.goals.models import Goal, GoalStatus
from apps.helpdesk.models import (
    SupportTicket,
    TicketCategory,
    TicketMessage,
    TicketPriority,
    TicketStatus,
)
from apps.insights.insight_service import SmartInsightService
from apps.insights.models import SmartInsight
from apps.leave_management.models import LeaveBalance, LeaveRequest, LeaveType
from apps.notifications.models import Notification
from apps.organization.models import Department, Designation, OrganizationProfile, Team
from apps.performance.models import PerformanceEvaluation, ReviewCycle

# Model imports across all 24 apps
from apps.permissions.models import SystemRole
from apps.permissions.services import PermissionService
from apps.projects.models import Project, ProjectMilestone, ProjectStatus
from apps.recognition.models import EmployeeRecognition, RecognitionCategory
from apps.shifts.models import CompanyHoliday, ShiftAssignment, WorkShift
from apps.skills.models import (
    EmployeeSkill,
    ProjectSkillRequirement,
    Skill,
    SkillCategory,
    SkillProficiency,
)
from apps.tasks.models import SubTask, Task, TaskComment, TaskPriority, TaskStatus
from apps.training.models import Course, EnrollmentStatus, TrainingEnrollment
from apps.workload.services import WorkloadCalculationService


class Command(BaseCommand):
    help = 'Seeds realistic enterprise demo data across all 24 modules of Smart EMS'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("--- Starting Smart EMS Enterprise Data Seeding ---"))

        # Clean existing data for clean re-seeding
        self.stdout.write("0. Purging previous sample records for clean re-seed...")
        Employee.objects.all().delete()
        User.objects.all().delete()
        Department.objects.all().delete()
        Team.objects.all().delete()
        Designation.objects.all().delete()
        WorkShift.objects.all().delete()
        CompanyHoliday.objects.all().delete()
        LeaveType.objects.all().delete()
        Project.objects.all().delete()
        SkillCategory.objects.all().delete()
        Skill.objects.all().delete()
        Goal.objects.all().delete()
        ReviewCycle.objects.all().delete()
        PerformanceEvaluation.objects.all().delete()
        Course.objects.all().delete()
        RecognitionCategory.objects.all().delete()
        AssetCategory.objects.all().delete()
        ExpenseCategory.objects.all().delete()
        TicketCategory.objects.all().delete()
        DocumentCategory.objects.all().delete()
        Announcement.objects.all().delete()
        CompanyEvent.objects.all().delete()
        Notification.objects.all().delete()
        SmartInsight.objects.all().delete()
        AuditLog.objects.all().delete()

        # 1. Initialize RBAC Roles & Permissions
        self.stdout.write("1. Initializing RBAC Roles & Permissions...")
        PermissionService.initialize_default_roles()

        # 2. System Settings & Organization Profile
        self.stdout.write("2. Creating Organization Profile & System Settings...")
        _org, _ = OrganizationProfile.objects.update_or_create(
            id=1,
            defaults={
                'name': 'Bharat Enterprise Solutions India Pvt. Ltd.',
                'registration_number': 'CIN-U72200KA2026PTC199842',
                'tax_id': 'GSTIN-29AABCU9603R1ZM',
                'email': 'contact@bharat-enterprise.in',
                'phone': '+91 (80) 4123-8899',
                'website': 'https://www.bharat-enterprise.internal',
                'address': 'Embassy TechVillage, Tower 2B, Outer Ring Road, Devarabeesanahalli',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'postal_code': '560103',
                'country': 'India',
                'currency': 'INR',
                'fiscal_year_start_month': 4,
            }
        )

        settings_data = [
            ('COMPANY_NAME', 'NovaTech Enterprise Solutions Inc.', 'GENERAL', 'Official entity company name'),
            ('MAX_FAILED_LOGINS', '5', 'SECURITY', 'Lockout account after consecutive failed attempts'),
            ('SESSION_TIMEOUT_MINUTES', '120', 'SECURITY', 'Inactivity session expiration threshold'),
            ('ATTENDANCE_GRACE_PERIOD', '15', 'ATTENDANCE', 'Grace minutes before marking attendance as late'),
            ('ANNUAL_LEAVE_QUOTA', '18', 'LEAVE', 'Default annual casual/earned leave quota per employee'),
            ('NOTIFICATION_EMAIL_ENABLED', 'True', 'NOTIFICATIONS', 'Broadcast email notifications'),
        ]
        for key, val, cat, desc in settings_data:
            SystemSetting.objects.update_or_create(
                key=key,
                defaults={'value': val, 'category': cat, 'description': desc}
            )

        BackupConfiguration.objects.update_or_create(
            id=1,
            defaults={
                'backup_type': 'FULL_DATABASE_SNAPSHOT',
                'frequency': 'DAILY_MIDNIGHT',
                'storage_location': 'local_backups/database/',
                'status': 'HEALTHY_AND_ACTIVE',
                'retention_days': 30,
                'last_backup_at': timezone.now() - timedelta(hours=8)
            }
        )

        # 3. Departments, Teams, and Designations
        self.stdout.write("3. Creating Departments, Teams, and Designations...")
        depts = {
            'ENG': Department.objects.create(name='Engineering & Technology', code='ENG', budget=Decimal('1500000.00'), location='Building A, Floor 4'),
            'HR': Department.objects.create(name='People Operations & HR', code='HR', budget=Decimal('400000.00'), location='Building A, Floor 2'),
            'SALES': Department.objects.create(name='Global Sales & Marketing', code='SALES', budget=Decimal('900000.00'), location='Building B, Floor 1'),
            'PROD': Department.objects.create(name='Product Strategy & UX', code='PROD', budget=Decimal('650000.00'), location='Building A, Floor 3'),
            'FIN': Department.objects.create(name='Finance, Legal & Ops', code='FIN', budget=Decimal('500000.00'), location='Building B, Floor 2'),
        }

        teams = {
            'BACKEND': Team.objects.create(name='Core Backend Engineering', code='ENG-BE', department=depts['ENG']),
            'FRONTEND': Team.objects.create(name='Web & UI Frontend', code='ENG-FE', department=depts['ENG']),
            'DEVOPS': Team.objects.create(name='Cloud Infrastructure & DevOps', code='ENG-OPS', department=depts['ENG']),
            'TALENT': Team.objects.create(name='Talent Acquisition & Culture', code='HR-TALENT', department=depts['HR']),
            'ENTERPRISE_SALES': Team.objects.create(name='Enterprise Accounts', code='SALES-ENT', department=depts['SALES']),
            'PRODUCT_CORE': Team.objects.create(name='Platform Product', code='PROD-CORE', department=depts['PROD']),
            'FIN_OPS': Team.objects.create(name='Treasury & Accounting', code='FIN-OPS', department=depts['FIN']),
        }

        desigs = {
            'CTO': Designation.objects.create(title='Chief Technology Officer', code='EXEC-CTO', department=depts['ENG'], grade_level='EXEC-1', min_salary=Decimal('180000.00'), max_salary=Decimal('250000.00')),
            'HR_DIR': Designation.objects.create(title='Director of People & Culture', code='HR-DIR', department=depts['HR'], grade_level='DIR-1', min_salary=Decimal('120000.00'), max_salary=Decimal('160000.00')),
            'ENG_LEAD': Designation.objects.create(title='Lead Software Architect', code='ENG-ARCH', department=depts['ENG'], grade_level='L5', min_salary=Decimal('130000.00'), max_salary=Decimal('170000.00')),
            'SR_DEV': Designation.objects.create(title='Senior Full-Stack Engineer', code='ENG-SR', department=depts['ENG'], grade_level='L4', min_salary=Decimal('105000.00'), max_salary=Decimal('140000.00')),
            'DEV': Designation.objects.create(title='Software Engineer II', code='ENG-MID', department=depts['ENG'], grade_level='L3', min_salary=Decimal('80000.00'), max_salary=Decimal('105000.00')),
            'DEVOPS_ENG': Designation.objects.create(title='DevOps & SRE Engineer', code='ENG-OPS', department=depts['ENG'], grade_level='L4', min_salary=Decimal('110000.00'), max_salary=Decimal('145000.00')),
            'HR_SPEC': Designation.objects.create(title='Human Resources Specialist', code='HR-SPEC', department=depts['HR'], grade_level='L3', min_salary=Decimal('65000.00'), max_salary=Decimal('85000.00')),
            'PROD_MGR': Designation.objects.create(title='Senior Product Manager', code='PROD-MGR', department=depts['PROD'], grade_level='L5', min_salary=Decimal('125000.00'), max_salary=Decimal('160000.00')),
            'SALES_EXEC': Designation.objects.create(title='Senior Account Executive', code='SALES-EXEC', department=depts['SALES'], grade_level='L4', min_salary=Decimal('85000.00'), max_salary=Decimal('120000.00')),
            'FIN_ANALYST': Designation.objects.create(title='Senior Financial Analyst', code='FIN-ANL', department=depts['FIN'], grade_level='L4', min_salary=Decimal('90000.00'), max_salary=Decimal('120000.00')),
        }

        # 4. Shifts & Holidays
        self.stdout.write("4. Creating Work Shifts and Company Holidays...")
        gen_shift = WorkShift.objects.create(name='General Day Shift', code='GEN-0900', start_time=time(9, 0), end_time=time(17, 30), grace_period_minutes=15, full_day_hours=Decimal('8.0'), half_day_hours=Decimal('4.0'))
        WorkShift.objects.create(name='Morning Shift', code='MRN-0800', start_time=time(8, 0), end_time=time(16, 30), grace_period_minutes=15, full_day_hours=Decimal('8.0'), half_day_hours=Decimal('4.0'))

        holidays = [
            ('New Year Holiday', date(2026, 1, 1), 'Global New Year Observance'),
            ('Republic Day', date(2026, 1, 26), 'National Republic Day of India'),
            ('Maha Shivratri', date(2026, 2, 15), 'Gazetted Public Holiday'),
            ('Holi (Festival of Colours)', date(2026, 3, 4), 'National Festive Holiday'),
            ('Eid-ul-Fitr', date(2026, 3, 20), 'Gazetted Public Holiday'),
            ('Independence Day', date(2026, 8, 15), 'National Independence Day of India'),
            ('Gandhi Jayanti', date(2026, 10, 2), 'National Holiday — Mahatma Gandhi Birthday'),
            ('Dussehra (Vijayadashami)', date(2026, 10, 20), 'National Festive Holiday'),
            ('Diwali (Deepavali)', date(2026, 11, 8), 'Festival of Lights Celebration'),
            ('Christmas Holiday', date(2026, 12, 25), 'Christmas Observance'),
        ]
        for h_name, h_date, h_desc in holidays:
            CompanyHoliday.objects.create(name=h_name, date=h_date, description=h_desc)

        # 5. Core Users and 28 Complete Employee Profiles
        self.stdout.write("5. Creating 28 Employees with complete 360° profile attributes (Indian Workforce Roster)...")

        # Base role users with Indian usernames as primary accounts
        admin_user = User.objects.create_superuser(username='aarav.sharma', email='aarav.sharma@novatech-india.com', password='Admin@12345', role=SystemRole.ADMIN)
        hr_user = User.objects.create_user(username='priya.patel', email='priya.patel@novatech-india.com', password='Admin@12345', role=SystemRole.HR)
        mgr_user = User.objects.create_user(username='rajesh.kumar', email='rajesh.kumar@novatech-india.com', password='Admin@12345', role=SystemRole.MANAGER)
        emp_user = User.objects.create_user(username='sneha.iyer', email='sneha.iyer@novatech-india.com', password='Admin@12345', role=SystemRole.EMPLOYEE)

        # Also create role shortcut accounts for quick multi-role evaluation
        admin_alias = User.objects.create_superuser(username='admin', email='admin.system@novatech-india.com', password='Admin@12345', role=SystemRole.ADMIN)
        hr_alias = User.objects.create_user(username='hrmanager', email='hr.system@novatech-india.com', password='Admin@12345', role=SystemRole.HR)
        mgr_alias = User.objects.create_user(username='manager', email='manager.system@novatech-india.com', password='Admin@12345', role=SystemRole.MANAGER)
        emp_alias = User.objects.create_user(username='employee', email='employee.system@novatech-india.com', password='Admin@12345', role=SystemRole.EMPLOYEE)

        # Indian Employee metadata roster
        raw_employees = [
            # 1. Admin / Executive (Aarav Sharma)
            ('EMP-1001', 'Aarav', 'Sharma', 'aarav.sharma@novatech-india.com', '+91-98765-01001', '1982-04-12', Gender.MALE, depts['ENG'], None, desigs['CTO'], None, admin_user),
            # 2. HR Director (Priya Patel)
            ('EMP-1002', 'Priya', 'Patel', 'priya.patel@novatech-india.com', '+91-98765-01002', '1986-09-22', Gender.FEMALE, depts['HR'], teams['TALENT'], desigs['HR_DIR'], None, hr_user),
            # 3. Team Manager / Lead Architect (Rajesh Kumar)
            ('EMP-1003', 'Rajesh', 'Kumar', 'rajesh.kumar@novatech-india.com', '+91-98765-01003', '1988-11-05', Gender.MALE, depts['ENG'], teams['BACKEND'], desigs['ENG_LEAD'], None, mgr_user),
            # 4. Senior Software Engineer (Sneha Iyer)
            ('EMP-1004', 'Sneha', 'Iyer', 'sneha.iyer@novatech-india.com', '+91-98765-01004', '1992-06-18', Gender.FEMALE, depts['ENG'], teams['BACKEND'], desigs['SR_DEV'], None, emp_user),
            # Role Shortcut Linked Profiles (Ensures 'admin', 'hrmanager', 'manager', 'employee' have full Employee data)
            ('EMP-1000', 'Aarav', 'Sharma (Admin)', 'admin.system@novatech-india.com', '+91-98765-01000', '1980-01-01', Gender.MALE, depts['ENG'], None, desigs['CTO'], None, admin_alias),
            ('EMP-1002A', 'Priya', 'Patel (HR Lead)', 'hr.system@novatech-india.com', '+91-98765-01002A', '1986-09-22', Gender.FEMALE, depts['HR'], teams['TALENT'], desigs['HR_DIR'], None, hr_alias),
            ('EMP-1003A', 'Rajesh', 'Kumar (Manager)', 'manager.system@novatech-india.com', '+91-98765-01003A', '1988-11-05', Gender.MALE, depts['ENG'], teams['BACKEND'], desigs['ENG_LEAD'], None, mgr_alias),
            ('EMP-1004A', 'Sneha', 'Iyer (Staff Dev)', 'employee.system@novatech-india.com', '+91-98765-01004A', '1992-06-18', Gender.FEMALE, depts['ENG'], teams['BACKEND'], desigs['SR_DEV'], None, emp_alias),
            # 5-28: Additional Indian Staff across departments
            ('EMP-1005', 'Vikram', 'Reddy', 'vikram.reddy@novatech-india.com', '+91-98765-01005', '1994-01-30', Gender.MALE, depts['ENG'], teams['BACKEND'], desigs['DEV'], None, None),
            ('EMP-1006', 'Ananya', 'Joshi', 'ananya.joshi@novatech-india.com', '+91-98765-01006', '1995-08-14', Gender.FEMALE, depts['ENG'], teams['FRONTEND'], desigs['SR_DEV'], None, None),
            ('EMP-1007', 'Rohan', 'Verma', 'rohan.verma@novatech-india.com', '+91-98765-01007', '1991-03-25', Gender.MALE, depts['ENG'], teams['FRONTEND'], desigs['DEV'], None, None),
            ('EMP-1008', 'Neha', 'Gupta', 'neha.gupta@novatech-india.com', '+91-98765-01008', '1990-12-03', Gender.FEMALE, depts['ENG'], teams['DEVOPS'], desigs['DEVOPS_ENG'], None, None),
            ('EMP-1009', 'Siddharth', 'Nair', 'siddharth.nair@novatech-india.com', '+91-98765-01009', '1993-07-19', Gender.MALE, depts['ENG'], teams['DEVOPS'], desigs['DEVOPS_ENG'], None, None),
            ('EMP-1010', 'Pooja', 'Rao', 'pooja.rao@novatech-india.com', '+91-98765-01010', '1996-05-11', Gender.FEMALE, depts['HR'], teams['TALENT'], desigs['HR_SPEC'], None, None),
            ('EMP-1011', 'Aditya', 'Mishra', 'aditya.mishra@novatech-india.com', '+91-98765-01011', '1987-10-09', Gender.MALE, depts['PROD'], teams['PRODUCT_CORE'], desigs['PROD_MGR'], None, None),
            ('EMP-1012', 'Kavita', 'Deshmukh', 'kavita.deshmukh@novatech-india.com', '+91-98765-01012', '1992-02-14', Gender.FEMALE, depts['SALES'], teams['ENTERPRISE_SALES'], desigs['SALES_EXEC'], None, None),
            ('EMP-1013', 'Arjun', 'Singhania', 'arjun.singhania@novatech-india.com', '+91-98765-01013', '1989-11-28', Gender.MALE, depts['SALES'], teams['ENTERPRISE_SALES'], desigs['SALES_EXEC'], None, None),
            ('EMP-1014', 'Meera', 'Nambiar', 'meera.nambiar@novatech-india.com', '+91-98765-01014', '1991-04-05', Gender.FEMALE, depts['FIN'], teams['FIN_OPS'], desigs['FIN_ANALYST'], None, None),
            ('EMP-1015', 'Karan', 'Kapoor', 'karan.kapoor@novatech-india.com', '+91-98765-01015', '1993-09-17', Gender.MALE, depts['ENG'], teams['BACKEND'], desigs['DEV'], None, None),
            ('EMP-1016', 'Deepika', 'Sen', 'deepika.sen@novatech-india.com', '+91-98765-01016', '1995-12-09', Gender.FEMALE, depts['ENG'], teams['BACKEND'], desigs['SR_DEV'], None, None),
            ('EMP-1017', 'Amitabh', 'Saxena', 'amitabh.saxena@novatech-india.com', '+91-98765-01017', '1990-08-20', Gender.MALE, depts['ENG'], teams['FRONTEND'], desigs['DEV'], None, None),
            ('EMP-1018', 'Ishita', 'Banerjee', 'ishita.banerjee@novatech-india.com', '+91-98765-01018', '1994-06-02', Gender.FEMALE, depts['ENG'], teams['FRONTEND'], desigs['DEV'], None, None),
            ('EMP-1019', 'Nikhil', 'Choudhury', 'nikhil.choudhury@novatech-india.com', '+91-98765-01019', '1988-05-16', Gender.MALE, depts['SALES'], teams['ENTERPRISE_SALES'], desigs['SALES_EXEC'], None, None),
            ('EMP-1020', 'Ritu', 'Bhattacharya', 'ritu.bhattacharya@novatech-india.com', '+91-98765-01020', '1993-10-31', Gender.FEMALE, depts['PROD'], teams['PRODUCT_CORE'], desigs['PROD_MGR'], None, None),
            ('EMP-1021', 'Sanjay', 'Kulkarni', 'sanjay.kulkarni@novatech-india.com', '+91-98765-01021', '1985-06-07', Gender.MALE, depts['FIN'], teams['FIN_OPS'], desigs['FIN_ANALYST'], None, None),
            ('EMP-1022', 'Swati', 'Agarwal', 'swati.agarwal@novatech-india.com', '+91-98765-01022', '1992-01-23', Gender.FEMALE, depts['HR'], teams['TALENT'], desigs['HR_SPEC'], None, None),
            ('EMP-1023', 'Varun', 'Hegde', 'varun.hegde@novatech-india.com', '+91-98765-01023', '1997-05-09', Gender.MALE, depts['ENG'], teams['BACKEND'], desigs['DEV'], None, None),
            ('EMP-1024', 'Divya', 'Menon', 'divya.menon@novatech-india.com', '+91-98765-01024', '1991-07-28', Gender.FEMALE, depts['PROD'], teams['PRODUCT_CORE'], desigs['PROD_MGR'], None, None),
            ('EMP-1025', 'Manish', 'Tiwari', 'manish.tiwari@novatech-india.com', '+91-98765-01025', '1989-08-18', Gender.MALE, depts['ENG'], teams['DEVOPS'], desigs['DEVOPS_ENG'], None, None),
            ('EMP-1026', 'Sunita', 'Pillai', 'sunita.pillai@novatech-india.com', '+91-98765-01026', '1994-04-05', Gender.FEMALE, depts['SALES'], teams['ENTERPRISE_SALES'], desigs['SALES_EXEC'], None, None),
            ('EMP-1027', 'Harsh', 'Vardhan', 'harsh.vardhan@novatech-india.com', '+91-98765-01027', '1998-01-10', Gender.MALE, depts['ENG'], teams['FRONTEND'], desigs['DEV'], None, None),
            ('EMP-1028', 'Rashmi', 'Chatterjee', 'rashmi.chatterjee@novatech-india.com', '+91-98765-01028', '1990-04-28', Gender.FEMALE, depts['HR'], teams['TALENT'], desigs['HR_SPEC'], None, None),
        ]

        created_employees = []
        lead_manager = None

        indian_cities = [
            ('Bengaluru', 'Karnataka', '560103'),
            ('Mumbai', 'Maharashtra', '400051'),
            ('Hyderabad', 'Telangana', '500081'),
            ('Pune', 'Maharashtra', '411057'),
            ('Gurugram', 'Haryana', '122002'),
            ('Chennai', 'Tamil Nadu', '600096'),
            ('Noida', 'Uttar Pradesh', '201301'),
        ]

        indian_institutions = [
            'Indian Institute of Technology (IIT) Bombay',
            'Indian Institute of Technology (IIT) Delhi',
            'Indian Institute of Technology (IIT) Madras',
            'Birla Institute of Technology and Science (BITS) Pilani',
            'International Institute of Information Technology (IIIT) Hyderabad',
            'National Institute of Technology (NIT) Trichy',
            'Delhi Technological University (DTU)',
            'Indian Institute of Management (IIM) Bangalore',
        ]

        indian_banks = [
            ('HDFC Bank Ltd.', 'HDFC0001042', 'Koramangala 4th Block, Bengaluru'),
            ('State Bank of India (SBI)', 'SBIN0004512', 'BKC Main Branch, Mumbai'),
            ('ICICI Bank Ltd.', 'ICIC0000892', 'Cyber Gateway Branch, HITEC City, Hyderabad'),
            ('Axis Bank Ltd.', 'UTIB0000541', 'Magarpatta Cybercity, Pune'),
            ('Kotak Mahindra Bank', 'KKBK0000214', 'Golf Course Road, Gurugram'),
        ]

        for i, (code, fn, ln, em, ph, dob, gdr, dpt, tm, dsg, mgr, usr) in enumerate(raw_employees):
            if not usr:
                usr = User.objects.create_user(
                    username=f"{fn.lower()}.{ln.lower()}",
                    email=em,
                    password="Password@123",
                    role=SystemRole.EMPLOYEE
                )

            city_info = indian_cities[i % len(indian_cities)]
            bank_info = indian_banks[i % len(indian_banks)]
            inst_name = indian_institutions[i % len(indian_institutions)]

            emp = Employee.objects.create(
                user=usr,
                employee_id=code,
                first_name=fn,
                last_name=ln,
                email=em,
                phone=ph,
                date_of_birth=datetime.strptime(dob, '%Y-%m-%d').date(),
                gender=gdr,
                date_of_joining=date(2023, 1, 15) + timedelta(days=random.randint(0, 700)),
                department=dpt,
                team=tm,
                designation=dsg,
                reporting_manager=lead_manager if lead_manager else None,
                employment_status=EmploymentStatus.ACTIVE,
                employment_type=EmploymentType.FULL_TIME,
                current_address=f"Plot No. {random.randint(12, 140)}, Phase {random.randint(1, 4)}, Tech Park Enclave",
                city=city_info[0],
                state=city_info[1],
                postal_code=city_info[2],
                country='India',
                emergency_contact_name=f"{fn}'s Family Emergency Contact",
                emergency_contact_phone='+91-98765-99999',
                emergency_contact_relation='Spouse / Parent / Next of Kin'
            )

            # Bank details (Indian NEFT / RTGS / IFSC)
            EmployeeBankDetail.objects.create(
                employee=emp,
                bank_name=bank_info[0],
                account_number=f"501002384{random.randint(1000, 9999)}",
                routing_or_ifsc_code=bank_info[1],
                branch_name=bank_info[2],
                account_type='SAVINGS'
            )

            # Education
            EmployeeEducation.objects.create(
                employee=emp,
                degree='Bachelor of Technology (B.Tech)' if dpt.code == 'ENG' else 'Master of Business Administration (MBA)',
                field_of_study='Computer Science & Engineering' if dpt.code == 'ENG' else 'Strategic Management & Finance',
                institution=inst_name,
                start_year=2010,
                end_year=2014,
                grade_or_gpa='8.8 / 10.0 CGPA'
            )

            # Experience
            EmployeeExperience.objects.create(
                employee=emp,
                job_title='Senior Software Engineer' if dpt.code == 'ENG' else 'Senior Operations Specialist',
                company_name='Infosys & Tata Consultancy Tech Labs',
                start_date=date(2015, 6, 1),
                end_date=date(2022, 12, 1),
                is_current=False,
                description='Architected enterprise services, API microservices, distributed workflows, and cross-functional deliverables.'
            )

            created_employees.append(emp)
            if code == 'EMP-1003':
                lead_manager = emp

        # Set department heads & team leads
        depts['ENG'].head_of_department = created_employees[0]
        depts['ENG'].save()
        depts['HR'].head_of_department = created_employees[1]
        depts['HR'].save()
        teams['BACKEND'].team_lead = created_employees[2]
        teams['BACKEND'].save()

        # Update remaining employees to report to Alex Morgan or Sarah Jenkins
        for emp in created_employees[3:]:
            emp.reporting_manager = created_employees[2] if emp.department.code == 'ENG' else created_employees[1]
            emp.save()

        # Assign work shifts
        for emp in created_employees:
            ShiftAssignment.objects.create(
                employee=emp,
                shift=gen_shift,
                start_date=date(2025, 1, 1),
                is_active=True
            )

        # 6. 45 Days of Attendance History
        self.stdout.write("6. Generating 45-day historical attendance records...")
        today = timezone.now().date()
        att_objs = []
        for emp in created_employees:
            for d in range(45, 0, -1):
                rec_date = today - timedelta(days=d)
                # Skip weekends
                if rec_date.weekday() in (5, 6):
                    continue

                # Attendance distribution: 88% Present on time, 8% Late, 4% Absent
                rnd = random.random()
                if rnd < 0.82:
                    in_time = time(8, 50 + random.randint(0, 9))
                    out_time = time(17, random.randint(30, 59))
                    att_objs.append(AttendanceRecord(
                        employee=emp,
                        date=rec_date,
                        check_in_time=in_time,
                        check_out_time=out_time,
                        total_working_hours=Decimal('8.50'),
                        status=AttendanceStatus.PRESENT,
                        is_late=False,
                        late_minutes=0
                    ))
                elif rnd < 0.94:
                    late_min = random.randint(18, 45)
                    in_time = time(9, late_min)
                    out_time = time(17, 30)
                    att_objs.append(AttendanceRecord(
                        employee=emp,
                        date=rec_date,
                        check_in_time=in_time,
                        check_out_time=out_time,
                        total_working_hours=Decimal('7.80'),
                        status=AttendanceStatus.PRESENT,
                        is_late=True,
                        late_minutes=late_min
                    ))
                else:
                    att_objs.append(AttendanceRecord(
                        employee=emp,
                        date=rec_date,
                        total_working_hours=Decimal('0.00'),
                        status=AttendanceStatus.ABSENT,
                        is_late=False,
                        late_minutes=0
                    ))

        AttendanceRecord.objects.bulk_create(att_objs)

        # 7. Leave Management (Types, Balances & Requests)
        self.stdout.write("7. Initializing Leave Types, Employee Balances, and Applications...")
        lt_casual = LeaveType.objects.create(name='Casual Leave', code='CL', days_per_year=Decimal('12.0'), is_paid=True)
        lt_sick = LeaveType.objects.create(name='Sick & Medical Leave', code='SL', days_per_year=Decimal('10.0'), is_paid=True)
        lt_earned = LeaveType.objects.create(name='Earned / Annual Vacation', code='EL', days_per_year=Decimal('15.0'), is_paid=True)

        for emp in created_employees:
            LeaveBalance.objects.create(employee=emp, leave_type=lt_casual, year=2026, total_allocated=Decimal('12.0'), used_days=Decimal('2.0'), pending_days=Decimal('0.0'))
            LeaveBalance.objects.create(employee=emp, leave_type=lt_sick, year=2026, total_allocated=Decimal('10.0'), used_days=Decimal('1.0'), pending_days=Decimal('0.0'))
            LeaveBalance.objects.create(employee=emp, leave_type=lt_earned, year=2026, total_allocated=Decimal('15.0'), used_days=Decimal('3.0'), pending_days=Decimal('0.0'))

        # Seed sample leave requests
        LeaveRequest.objects.create(employee=created_employees[3], leave_type=lt_casual, start_date=today + timedelta(days=5), end_date=today + timedelta(days=7), total_days=Decimal('3.0'), reason='Family relocation and personal matters.', status='PENDING')
        LeaveRequest.objects.create(employee=created_employees[4], leave_type=lt_sick, start_date=today - timedelta(days=12), end_date=today - timedelta(days=11), total_days=Decimal('2.0'), reason='Seasonal flu recovery.', status='APPROVED', reviewed_by=created_employees[1], reviewed_at=timezone.now() - timedelta(days=13))

        # 8. Projects & Tasks
        self.stdout.write("8. Creating Enterprise Projects, Milestones, and Kanban Deliverables...")
        prj1 = Project.objects.create(name='Cloud Infrastructure Modernization', code='PRJ-2026-001', manager=created_employees[2], start_date=date(2026, 1, 15), end_date=date(2026, 9, 30), budget=Decimal('350000.00'), progress_percentage=75, status=ProjectStatus.ACTIVE, description='Transition monolithic services into microservices on Kubernetes.')
        prj2 = Project.objects.create(name='Global Payroll & Tax Engine 2.0', code='PRJ-2026-002', manager=created_employees[2], start_date=date(2026, 2, 1), end_date=date(2026, 8, 15), budget=Decimal('220000.00'), progress_percentage=50, status=ProjectStatus.ACTIVE, description='Automated localized tax withholdings and direct payroll deposits.')
        prj3 = Project.objects.create(name='Enterprise Mobile Workforce App', code='PRJ-2026-003', manager=created_employees[10], start_date=date(2026, 3, 1), end_date=date(2026, 11, 30), budget=Decimal('180000.00'), progress_percentage=35, status=ProjectStatus.ACTIVE, description='Cross-platform mobile application for attendance check-ins and expenses.')

        for p in [prj1, prj2, prj3]:
            p.members.add(*created_employees[2:10])

        ProjectMilestone.objects.create(project=prj1, title='Architecture & VPC Setup', due_date=date(2026, 3, 15), is_completed=True, completion_date=date(2026, 3, 12))
        ProjectMilestone.objects.create(project=prj1, title='Zero-Downtime Database Migration', due_date=date(2026, 6, 30), is_completed=True, completion_date=date(2026, 6, 28))
        ProjectMilestone.objects.create(project=prj1, title='Disaster Recovery Failover Simulation', due_date=date(2026, 9, 15), is_completed=False)

        # 45 Tasks across all priorities and statuses
        task_titles = [
            ('TSK-101', 'Optimize PostgreSQL Query Execution Plans', prj1, created_employees[3], TaskPriority.URGENT, TaskStatus.IN_PROGRESS, 16.0, 10.0),
            ('TSK-102', 'Implement JWT Session Revocation & Blacklisting', prj1, created_employees[4], TaskPriority.HIGH, TaskStatus.REVIEW, 12.0, 12.0),
            ('TSK-103', 'Write Pytest Suite for Attendance Calculations', prj1, created_employees[5], TaskPriority.MEDIUM, TaskStatus.COMPLETED, 8.0, 8.0),
            ('TSK-104', 'Set up Prometheus & Grafana Metric Scrapers', prj1, created_employees[7], TaskPriority.HIGH, TaskStatus.IN_PROGRESS, 20.0, 14.0),
            ('TSK-105', 'Design Mobile Responsive Timesheet Grid', prj3, created_employees[6], TaskPriority.MEDIUM, TaskStatus.TODO, 14.0, 0.0),
            ('TSK-106', 'Build Multi-Currency Expense Conversion Engine', prj2, created_employees[3], TaskPriority.URGENT, TaskStatus.IN_PROGRESS, 18.0, 8.0),
            ('TSK-107', 'Configure CI/CD GitHub Actions Build Pipelines', prj1, created_employees[8], TaskPriority.HIGH, TaskStatus.COMPLETED, 10.0, 10.0),
            ('TSK-108', 'Integrate RBAC Permission Matrix Context Processor', prj1, created_employees[4], TaskPriority.MEDIUM, TaskStatus.COMPLETED, 6.0, 6.0),
            ('TSK-109', 'Develop Offline Local Chart Rendering Wrapper', prj3, created_employees[5], TaskPriority.LOW, TaskStatus.TODO, 8.0, 0.0),
            ('TSK-110', 'Conduct Security Vulnerability Audit Scan', prj1, created_employees[7], TaskPriority.URGENT, TaskStatus.IN_PROGRESS, 24.0, 12.0),
        ]

        for code, t_title, p, assignee, pri, st, est, act in task_titles:
            t = Task.objects.create(
                project=p,
                code=code,
                title=t_title,
                assigned_to=assignee,
                priority=pri,
                status=st,
                start_date=today - timedelta(days=10),
                due_date=today + timedelta(days=random.randint(2, 14)),
                estimated_hours=Decimal(str(est)),
                actual_hours=Decimal(str(act)),
                description=f"Detailed engineering deliverable for {t_title} adhering to internal standards."
            )
            SubTask.objects.create(task=t, title='Technical design review & peer signoff', is_completed=True)
            SubTask.objects.create(task=t, title='Automated test coverage verification', is_completed=(st == TaskStatus.COMPLETED))
            TaskComment.objects.create(task=t, author=created_employees[2], content='Sprint progress looks steady. Keep up the high test coverage.')

        # 9. Skills & Matrix Competencies
        self.stdout.write("9. Populating Skill Catalog & Competency Matrices...")
        sc_backend = SkillCategory.objects.create(name='Backend Engineering', description='Server-side languages, frameworks, and APIs')
        sc_frontend = SkillCategory.objects.create(name='Frontend & UI', description='Web client technologies and modern design systems')
        sc_cloud = SkillCategory.objects.create(name='Cloud & DevOps', description='Containerization, orchestration, and infrastructure')
        sc_data = SkillCategory.objects.create(name='Data & Analytics', description='Machine learning, data pipelines, and analytics')

        sk_python = Skill.objects.create(category=sc_backend, name='Python / Django', code='SK-PY')
        sk_k8s = Skill.objects.create(category=sc_cloud, name='Kubernetes & Docker', code='SK-K8S')
        Skill.objects.create(category=sc_data, name='Scikit-Learn & ML', code='SK-ML')
        Skill.objects.create(category=sc_frontend, name='JavaScript & UI Design', code='SK-JS')
        sk_sql = Skill.objects.create(category=sc_backend, name='PostgreSQL & DB Architecture', code='SK-SQL')

        for emp in created_employees:
            EmployeeSkill.objects.create(employee=emp, skill=sk_python, proficiency_level=SkillProficiency.ADVANCED if emp.department.code == 'ENG' else SkillProficiency.BEGINNER, years_of_experience=Decimal('5.0'), is_verified=True, verified_by=created_employees[2])
            EmployeeSkill.objects.create(employee=emp, skill=sk_sql, proficiency_level=SkillProficiency.EXPERT if emp.department.code == 'ENG' else SkillProficiency.INTERMEDIATE, years_of_experience=Decimal('6.0'), is_verified=True, verified_by=created_employees[2])
            EmployeeSkill.objects.create(employee=emp, skill=sk_k8s, proficiency_level=SkillProficiency.ADVANCED if emp.designation.code == 'ENG-OPS' else SkillProficiency.BEGINNER, years_of_experience=Decimal('3.5'), is_verified=True, verified_by=created_employees[2])

        # Project skill requirements
        ProjectSkillRequirement.objects.create(project=prj1, skill=sk_python, min_proficiency=SkillProficiency.ADVANCED)
        ProjectSkillRequirement.objects.create(project=prj1, skill=sk_k8s, min_proficiency=SkillProficiency.ADVANCED)

        # 10. Goals & OKRs
        self.stdout.write("10. Creating Goals and Key Results (OKRs)...")
        Goal.objects.create(employee=created_employees[3], title='Achieve 92% Code Test Coverage on Core Modules', target_metric='Pytest Coverage %', target_value=Decimal('92.0'), current_value=Decimal('88.5'), unit='%', start_date=date(2026, 1, 1), due_date=date(2026, 9, 30), progress_percentage=85, status=GoalStatus.IN_PROGRESS, description='Comprehensive automated test suites for models, services, and views.')
        Goal.objects.create(employee=created_employees[4], title='Reduce Database P99 Query Latency Below 50ms', target_metric='P99 Latency', target_value=Decimal('50.0'), current_value=Decimal('62.0'), unit='ms', start_date=date(2026, 2, 1), due_date=date(2026, 8, 31), progress_percentage=60, status=GoalStatus.IN_PROGRESS, description='Apply proper indexing, connection pooling, and queryset optimizations.')

        # 11. Performance Reviews
        self.stdout.write("11. Creating Performance Appraisal Cycles & Evaluations...")
        cycle = ReviewCycle.objects.create(title='Q1 2026 Corporate Performance Appraisal', code='REV-2026-Q1', start_date=date(2026, 3, 1), end_date=date(2026, 3, 31), is_active=False)
        PerformanceEvaluation.objects.create(
            cycle=cycle,
            employee=created_employees[3],
            evaluator=created_employees[2],
            technical_skills_rating=Decimal('4.80'),
            communication_rating=Decimal('4.50'),
            productivity_rating=Decimal('4.90'),
            leadership_rating=Decimal('4.20'),
            final_score=Decimal('4.60'),
            strengths='Exceptional architectural vision and reliable delivery cadence.',
            areas_of_improvement='Continue mentoring junior engineers during sprint reviews.',
            manager_comments='Exemplary top-tier contributor across the organization.',
            is_submitted=True
        )

        # 12. Training & Development
        self.stdout.write("12. Creating Training Courses and Certifications...")
        c1 = Course.objects.create(category=sc_cloud, title='Certified Kubernetes Administrator (CKA) Intensive', code='CRS-CKA-01', provider='Cloud Native Foundation', duration_hours=Decimal('36.0'), pass_score=80, is_active=True, description='Master container orchestration, networking, and cluster security.')
        c2 = Course.objects.create(category=sc_backend, title='Advanced Python Architecture & Asyncio', code='CRS-PY-02', provider='Internal Tech Academy', duration_hours=Decimal('24.0'), pass_score=75, is_active=True, description='Deep dive into modern Python design patterns and memory management.')

        TrainingEnrollment.objects.create(course=c1, employee=created_employees[3], status=EnrollmentStatus.COMPLETED, completion_date=date(2026, 2, 15), score=Decimal('94.0'), certificate_expiry_date=today + timedelta(days=45))
        TrainingEnrollment.objects.create(course=c2, employee=created_employees[4], status=EnrollmentStatus.IN_PROGRESS)

        # 13. Recognition & Feedback (Kudos)
        self.stdout.write("13. Creating Recognition Categories and Kudos Wall Posts...")
        rc_tech = RecognitionCategory.objects.create(name='Technical Excellence', badge_icon='bi-code-slash', points=100, description='Demonstrated outstanding technical skill and quality.')
        rc_team = RecognitionCategory.objects.create(name='Team Collaboration', badge_icon='bi-people-fill', points=75, description='Went above and beyond to support teammates.')

        EmployeeRecognition.objects.create(sender=created_employees[2], recipient=created_employees[3], category=rc_tech, title='Brilliant Database Refactoring', message='Sneha re-architected our database connection pooling and transaction locking mechanism, saving 45% query response time!')
        EmployeeRecognition.objects.create(sender=created_employees[3], recipient=created_employees[7], category=rc_team, title='Rapid DevOps Incident Resolution', message='Neha resolved the production deployment pipeline blocker in record time!')

        # 14. Asset Management
        self.stdout.write("14. Initializing Hardware & Corporate Asset Inventory...")
        ac_laptop = AssetCategory.objects.create(name='High-Performance Laptops', description='Laptops')
        AssetCategory.objects.create(name='UltraSharp 4K Displays', description='Monitors')

        for i, emp in enumerate(created_employees):
            Asset.objects.create(
                asset_id=f"AST-LAP-{1000 + i}",
                category=ac_laptop,
                name=f"MacBook Pro 16\" M3 Max ({emp.first_name})",
                serial_number=f"MBP-2026-SN{random.randint(10000, 99999)}",
                assigned_to=emp,
                assigned_date=emp.date_of_joining,
                purchase_date=date(2025, 6, 1),
                purchase_cost=Decimal('3499.00'),
                warranty_expiry_date=date(2028, 6, 1),
                status=AssetStatus.ASSIGNED
            )

        # 15. Expense Management
        self.stdout.write("15. Creating Expense Claims and Categories...")
        ec_travel = ExpenseCategory.objects.create(name='Client Travel & Lodging', description='Travel expenses')
        ec_equip = ExpenseCategory.objects.create(name='Remote Office Hardware', description='Hardware expenses')

        ExpenseClaim.objects.create(employee=created_employees[3], category=ec_equip, claim_number='CLM-2026-001', title='Ergonomic Desk Accessories', amount=Decimal('340.00'), expense_date=today - timedelta(days=8), status=ExpenseStatus.REIMBURSED, description='Ergonomic mechanical keyboard and vertical mouse for workstation.')
        ExpenseClaim.objects.create(employee=created_employees[4], category=ec_travel, claim_number='CLM-2026-002', title='PyCon India Conference Flight & Hotel', amount=Decimal('1250.00'), expense_date=today - timedelta(days=3), status=ExpenseStatus.PENDING, description='Travel expenses for representing company at technical conference.')

        # 16. Helpdesk & Support Tickets
        self.stdout.write("16. Creating Support Tickets & Discussion Threads...")
        tc_it = TicketCategory.objects.create(name='IT Hardware & Infrastructure', sla_resolution_hours=24, description='IT hardware tickets')
        tc_hr = TicketCategory.objects.create(name='Payroll & Benefits', sla_resolution_hours=48, description='HR inquiries')

        tkt1 = SupportTicket.objects.create(ticket_number='TKT-2026-001', category=tc_it, creator=created_employees[3], subject='Request VPN Access Token Refresh', priority=TicketPriority.MEDIUM, status=TicketStatus.RESOLVED, description='Need updated credentials for the secondary European AWS VPN endpoint.', resolution_notes='Generated new 2FA certificate and emailed securely.')
        TicketMessage.objects.create(ticket=tkt1, sender=created_employees[3], message='Please generate the token for my backup machine.')
        TicketMessage.objects.create(ticket=tkt1, sender=created_employees[7], message='Certificate issued and tested on VPN gateway.')

        SupportTicket.objects.create(ticket_number='TKT-2026-002', category=tc_hr, creator=created_employees[4], subject='Provident Fund (EPF) Voluntary Contribution Percentage Adjustment', priority=TicketPriority.LOW, status=TicketStatus.OPEN, description='Would like to increase monthly voluntary EPF / VPF deduction.')

        # 17. Document Management
        self.stdout.write("17. Uploading Document Records...")
        dc_emp = DocumentCategory.objects.create(name='Employment Contracts & Agreements', description='Employment contracts')
        dc_pol = DocumentCategory.objects.create(name='Corporate Compliance & Security Policies', description='Policies')

        EmployeeDocument.objects.create(title='Employee Non-Disclosure & IP Agreement', category=dc_emp, employee=created_employees[3], document_number='NDA-2026-042', is_company_wide=False)
        EmployeeDocument.objects.create(title='Enterprise Information Security Policy 2026', category=dc_pol, is_company_wide=True)

        # 18. Announcements & Company Events
        self.stdout.write("18. Creating Announcements & Company Events...")
        Announcement.objects.create(title='Annual Performance Appraisal Cycle 2026 Now Active', category=AnnouncementCategory.HR_UPDATE, content='All managers and employees are requested to complete self-evaluations and manager feedback by the end of the month.', publish_date=today - timedelta(days=3), is_pinned=True, created_by=created_employees[1])
        Announcement.objects.create(title='India Tech Innovation Summit & Hackathon', category=AnnouncementCategory.GENERAL, content='Join us next month for our 48-hour global innovation hackathon! Exciting prizes and project incubation opportunities.', publish_date=today - timedelta(days=1), is_pinned=False, created_by=created_employees[0])

        ev = CompanyEvent.objects.create(title='Quarterly Company Town Hall & Strategic Roadmap', event_date=timezone.now() + timedelta(days=7), location='Auditorium A & Live Stream', description='Executive leadership reviews Q2 milestones and reveals upcoming product launches.', registration_required=True)
        EventRegistration.objects.create(event=ev, employee=created_employees[3])
        EventRegistration.objects.create(event=ev, employee=created_employees[4])

        # 19. Notifications
        self.stdout.write("19. Generating User Notifications...")
        Notification.objects.create(recipient=admin_user, title='System Intelligence Analysis Ready', message='Local ML analytics completed daily scan with 0 errors.', category='SYSTEM')
        Notification.objects.create(recipient=emp_user, title='Leave Balance Updated', message='Your annual leave balance has been refreshed for 2026.', category='LEAVE')

        # 20. Audit Trail Records
        self.stdout.write("20. Initializing Audit Logs...")
        AuditLog.objects.create(user=admin_user, username='aarav.sharma', action=AuditAction.LOGIN, module='AUTHENTICATION', ip_address='127.0.0.1', description='Superuser admin logged in successfully.')
        AuditLog.objects.create(user=hr_user, username='priya.patel', action=AuditAction.APPROVE, module='LEAVE_MANAGEMENT', ip_address='127.0.0.1', description='Approved sick leave request for Vikram Reddy.')

        # 21. Execute Workload Calculations & Smart Insights ML Engine
        self.stdout.write("21. Executing Workload Scoring Engine...")
        WorkloadCalculationService.recalculate_all_workloads()

        self.stdout.write("22. Triggering Local Smart Insights Engine...")
        insights_count = SmartInsightService.run_full_system_analysis()

        self.stdout.write(self.style.SUCCESS(f"--- SUCCESS: Seeded full dataset with 28 employees and {insights_count} smart insights! ---"))
