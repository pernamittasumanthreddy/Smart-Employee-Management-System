import os

TEST_FILES = {
    "tests/__init__.py": "# tests package\n",
    
    "tests/test_authentication.py": """import pytest
from django.urls import reverse
from apps.authentication.models import User, LoginHistory
from apps.permissions.models import SystemRole

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(username='testuser', email='test@test.com', password='Password@123', role=SystemRole.EMPLOYEE)
    assert user.username == 'testuser'
    assert user.role == SystemRole.EMPLOYEE
    assert user.check_password('Password@123')

@pytest.mark.django_db
def test_login_view(client):
    user = User.objects.create_user(username='testlogin', email='login@test.com', password='Password@123')
    response = client.post(reverse('authentication:login'), {'username': 'testlogin', 'password': 'Password@123'})
    assert response.status_code == 302
""",

    "tests/test_permissions.py": """import pytest
from apps.permissions.models import Role, ModulePermission, SystemRole, SystemModule
from apps.permissions.services import PermissionService

@pytest.mark.django_db
def test_permission_initialization():
    PermissionService.initialize_default_roles()
    assert Role.objects.filter(code=SystemRole.ADMIN).exists()
    assert Role.objects.filter(code=SystemRole.EMPLOYEE).exists()
    admin_role = Role.objects.get(code=SystemRole.ADMIN)
    assert admin_role.permissions.count() > 0
""",

    "tests/test_organization.py": """import pytest
from decimal import Decimal
from apps.organization.models import Department, Team, Designation

@pytest.mark.django_db
def test_department_and_team():
    dept = Department.objects.create(name='Technology', code='TECH', budget=Decimal('50000.00'))
    team = Team.objects.create(name='Dev Team', code='DEV', department=dept)
    assert team.department == dept
    assert 'Technology' in str(dept)
""",

    "tests/test_employees.py": """import pytest
from datetime import date
from apps.authentication.models import User
from apps.employees.models import Employee, EmploymentStatus, Gender
from apps.employees.services import Employee360Service
from apps.organization.models import Department

@pytest.mark.django_db
def test_employee_and_360_service():
    user = User.objects.create_user(username='emp360', email='360@test.com', password='Password@123')
    dept = Department.objects.create(name='Engineering', code='ENG')
    emp = Employee.objects.create(
        user=user,
        employee_id='EMP-TEST-01',
        first_name='John',
        last_name='Doe',
        email='360@test.com',
        phone='1234567890',
        date_of_birth=date(1990, 1, 1),
        gender=Gender.MALE,
        date_of_joining=date(2025, 1, 1),
        department=dept,
        employment_status=EmploymentStatus.ACTIVE
    )
    assert emp.full_name == 'John Doe'
    profile_360 = Employee360Service.get_full_360_profile(emp)
    assert profile_360['employee'] == emp
""",

    "tests/test_attendance.py": """import pytest
from datetime import date, time
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.attendance.services import AttendanceService
from apps.shifts.models import WorkShift, ShiftAssignment

@pytest.mark.django_db
def test_attendance_punch():
    user = User.objects.create_user(username='attuser', email='att@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-ATT-01', first_name='Att', last_name='User', email='att@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    shift = WorkShift.objects.create(name='Day', code='DAY', start_time=time(9, 0), end_time=time(17, 30))
    ShiftAssignment.objects.create(employee=emp, shift=shift, start_date=date(2025, 1, 1))

    rec, success, msg = AttendanceService.check_in(emp)
    assert success is True
    assert rec.check_in_time is not None
    assert rec.status == AttendanceStatus.PRESENT

    rec_out, success_out, msg_out = AttendanceService.check_out(emp)
    assert success_out is True
    assert rec_out.check_out_time is not None
    assert rec_out.total_working_hours >= Decimal('0.00')
""",

    "tests/test_leave_management.py": """import pytest
from datetime import date, timedelta
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.leave_management.models import LeaveType, LeaveBalance, LeaveRequest
from apps.leave_management.services import LeaveService

@pytest.mark.django_db
def test_leave_service_request_and_approval():
    user = User.objects.create_user(username='leaveuser', email='leave@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-LV-01', first_name='Leave', last_name='User', email='leave@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    lt = LeaveType.objects.create(name='Casual', code='CL', days_per_year=Decimal('12.0'))
    bal = LeaveBalance.objects.create(employee=emp, leave_type=lt, year=2026, total_allocated=Decimal('12.0'))

    req, success, msg = LeaveService.apply_leave(emp, lt, date(2026, 6, 1), date(2026, 6, 3), 'Vacation')
    assert success is True
    assert req.total_days == Decimal('3.0')
    assert req.status == 'PENDING'

    approved, app_success, app_msg = LeaveService.approve_leave(req, reviewer=emp)
    assert app_success is True
    assert approved.status == 'APPROVED'
    bal.refresh_from_db()
    assert bal.used_days == Decimal('3.0')
""",

    "tests/test_workload.py": """import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.projects.models import Project
from apps.tasks.models import Task, TaskPriority, TaskStatus
from apps.workload.services import WorkloadCalculationService

@pytest.mark.django_db
def test_workload_calculation():
    user = User.objects.create_user(username='wluser', email='wl@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-WL-01', first_name='Work', last_name='Load', email='wl@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    prj = Project.objects.create(name='Project A', code='PRJ-A', start_date=date(2026, 1, 1))
    Task.objects.create(project=prj, code='TSK-01', title='Task 1', assigned_to=emp, priority=TaskPriority.URGENT, status=TaskStatus.IN_PROGRESS, due_date=date(2026, 8, 30), estimated_hours=Decimal('10.0'))

    metric = WorkloadCalculationService.calculate_for_employee(emp)
    assert metric.workload_score > 0
    assert metric.active_tasks_count == 1
""",

    "tests/test_projects.py": """import pytest
from datetime import date
from apps.projects.models import Project, ProjectMilestone, ProjectStatus
from apps.tasks.models import Task, TaskStatus

@pytest.mark.django_db
def test_project_progress():
    prj = Project.objects.create(name='Apollo Mission', code='PRJ-APOLLO', start_date=date(2026, 1, 1), status=ProjectStatus.ACTIVE)
    Task.objects.create(project=prj, code='T1', title='T1', due_date=date(2026, 5, 1), status=TaskStatus.COMPLETED)
    Task.objects.create(project=prj, code='T2', title='T2', due_date=date(2026, 5, 1), status=TaskStatus.TODO)
    prj.recalculate_progress()
    assert prj.progress_percentage == 50
""",

    "tests/test_tasks.py": """import pytest
from datetime import date
from apps.projects.models import Project
from apps.tasks.models import Task, SubTask, TaskComment

@pytest.mark.django_db
def test_task_subtasks():
    prj = Project.objects.create(name='Task Project', code='PRJ-TSK', start_date=date(2026, 1, 1))
    t = Task.objects.create(project=prj, code='TSK-1', title='Core API', due_date=date(2026, 9, 1))
    s1 = SubTask.objects.create(task=t, title='Subtask A', is_completed=True)
    s2 = SubTask.objects.create(task=t, title='Subtask B', is_completed=False)
    assert t.subtasks.count() == 2
""",

    "tests/test_skills.py": """import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.skills.models import SkillCategory, Skill, EmployeeSkill, SkillProficiency

@pytest.mark.django_db
def test_skills():
    user = User.objects.create_user(username='skuser', email='sk@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-SK-01', first_name='Skill', last_name='User', email='sk@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cat = SkillCategory.objects.create(name='Programming')
    sk = Skill.objects.create(category=cat, name='Python', code='PY')
    es = EmployeeSkill.objects.create(employee=emp, skill=sk, proficiency_level=SkillProficiency.ADVANCED, years_of_experience=Decimal('4.0'))
    assert es.proficiency_level == SkillProficiency.ADVANCED
""",

    "tests/test_goals.py": """import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.goals.models import Goal, GoalStatus

@pytest.mark.django_db
def test_goal_progress():
    user = User.objects.create_user(username='gluser', email='gl@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-GL-01', first_name='Goal', last_name='User', email='gl@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    goal = Goal.objects.create(employee=emp, title='Target OKR', target_metric='Revenue', target_value=Decimal('100.0'), current_value=Decimal('80.0'), progress_percentage=80, start_date=date(2026, 1, 1), due_date=date(2026, 12, 31))
    assert goal.progress_percentage == 80
""",

    "tests/test_performance.py": """import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.performance.models import ReviewCycle, PerformanceEvaluation

@pytest.mark.django_db
def test_performance_review():
    user = User.objects.create_user(username='perfuser', email='perf@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-PF-01', first_name='Perf', last_name='User', email='perf@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cycle = ReviewCycle.objects.create(title='Q1 Appraisal', code='Q1-2026', start_date=date(2026, 1, 1), end_date=date(2026, 3, 31))
    eval_obj = PerformanceEvaluation.objects.create(
        cycle=cycle,
        employee=emp,
        technical_skills_rating=Decimal('4.5'),
        communication_rating=Decimal('4.0'),
        productivity_rating=Decimal('4.5'),
        leadership_rating=Decimal('4.0'),
        final_score=Decimal('4.25'),
        is_submitted=True
    )
    assert eval_obj.final_score == Decimal('4.25')
""",

    "tests/test_training.py": """import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.training.models import Course, TrainingEnrollment, EnrollmentStatus

@pytest.mark.django_db
def test_course_enrollment():
    user = User.objects.create_user(username='trainuser', email='train@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-TR-01', first_name='Train', last_name='User', email='train@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    c = Course.objects.create(title='Cybersecurity 101', code='SEC-101', duration_hours=Decimal('8.0'), pass_score=70)
    enr = TrainingEnrollment.objects.create(course=c, employee=emp, status=EnrollmentStatus.COMPLETED, score=Decimal('90.0'))
    assert enr.status == EnrollmentStatus.COMPLETED
""",

    "tests/test_recognition.py": """import pytest
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.recognition.models import RecognitionCategory, EmployeeRecognition
from datetime import date

@pytest.mark.django_db
def test_kudos():
    u1 = User.objects.create_user(username='u1', email='u1@test.com', password='Password@123')
    u2 = User.objects.create_user(username='u2', email='u2@test.com', password='Password@123')
    e1 = Employee.objects.create(user=u1, employee_id='EMP-K1', first_name='E1', last_name='User', email='u1@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    e2 = Employee.objects.create(user=u2, employee_id='EMP-K2', first_name='E2', last_name='User', email='u2@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cat = RecognitionCategory.objects.create(name='Speed', points=50)
    rec = EmployeeRecognition.objects.create(sender=e1, recipient=e2, category=cat, title='Great Work', message='Thanks for quick help!')
    assert rec.recipient == e2
""",

    "tests/test_assets.py": """import pytest
from datetime import date
from apps.assets.models import AssetCategory, Asset, AssetStatus

@pytest.mark.django_db
def test_assets():
    cat = AssetCategory.objects.create(name='Laptops')
    asset = Asset.objects.create(asset_id='AST-01', category=cat, name='ThinkPad X1', serial_number='TP-9921', purchase_date=date(2025, 1, 1), status=AssetStatus.AVAILABLE)
    assert asset.status == AssetStatus.AVAILABLE
""",

    "tests/test_expenses.py": """import pytest
from datetime import date
from decimal import Decimal
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.expenses.models import ExpenseCategory, ExpenseClaim, ExpenseStatus

@pytest.mark.django_db
def test_expenses():
    user = User.objects.create_user(username='expuser', email='exp@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-EXP-01', first_name='Exp', last_name='User', email='exp@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cat = ExpenseCategory.objects.create(name='Travel')
    claim = ExpenseClaim.objects.create(employee=emp, category=cat, claim_number='CLM-001', title='Hotel stay', amount=Decimal('200.00'), expense_date=date(2026, 5, 1), description='Lodging')
    assert claim.status == ExpenseStatus.PENDING
""",

    "tests/test_helpdesk.py": """import pytest
from datetime import date
from apps.authentication.models import User
from apps.employees.models import Employee
from apps.helpdesk.models import TicketCategory, SupportTicket, TicketStatus

@pytest.mark.django_db
def test_helpdesk():
    user = User.objects.create_user(username='hduser', email='hd@test.com', password='Password@123')
    emp = Employee.objects.create(user=user, employee_id='EMP-HD-01', first_name='HD', last_name='User', email='hd@test.com', phone='1234', date_of_birth=date(1990, 1, 1), date_of_joining=date(2025, 1, 1))
    cat = TicketCategory.objects.create(name='IT')
    tkt = SupportTicket.objects.create(ticket_number='TKT-01', category=cat, creator=emp, subject='Monitor broken', description='No display')
    assert tkt.status == TicketStatus.OPEN
""",

    "tests/test_insights.py": """import pytest
from apps.insights.insight_service import SmartInsightService
from apps.insights.models import SmartInsight

@pytest.mark.django_db
def test_insights_generation():
    count = SmartInsightService.run_full_system_analysis()
    assert isinstance(count, int)
""",

    "tests/test_administration.py": """import pytest
from apps.authentication.models import User
from apps.administration.models import AuditLog, AuditAction, BackupConfiguration

@pytest.mark.django_db
def test_audit_logs():
    user = User.objects.create_user(username='admuser', email='adm@test.com', password='Password@123')
    log = AuditLog.objects.create(user=user, username='admuser', action=AuditAction.CREATE, module='EMPLOYEES', description='Created employee')
    assert log.action == AuditAction.CREATE
"""
}

for filepath, content in TEST_FILES.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {filepath}")

print("Test suite updated!")
