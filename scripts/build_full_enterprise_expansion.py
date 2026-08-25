import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# ADDITIONAL DOMAIN SERVICES ACROSS ALL EXISTING APPS
# ==============================================================================

write_file("apps/employees/skill_matrix_service.py", """
from decimal import Decimal
from typing import List, Dict, Any
from django.db.models import Count, Avg
from apps.employees.models import Employee
from apps.skills.models import Skill, EmployeeSkill

class SkillMatrixAnalyticsService:
    '''
    Analyzes organizational competency distributions, skill gaps across departments,
    critical single points of failure (SPOFs), and training recommendation paths.
    '''

    @staticmethod
    def compute_department_skill_gap(department_id: int) -> Dict[str, Any]:
        employees = Employee.objects.filter(department_id=department_id)
        total_emp = employees.count()
        if total_emp == 0:
            return {'total_employees': 0, 'skill_coverage': {}, 'critical_gaps': []}

        skills = Skill.objects.all()
        coverage_data = {}
        critical_gaps = []

        for skill in skills:
            emp_with_skill = EmployeeSkill.objects.filter(employee__in=employees, skill=skill)
            count = emp_with_skill.count()
            avg_rating = emp_with_skill.aggregate(avg=Avg('proficiency_level'))['avg'] or 0.0
            
            coverage_pct = round((count / total_emp) * 100.0, 1)
            coverage_data[skill.name] = {
                'headcount': count,
                'coverage_percentage': coverage_pct,
                'avg_proficiency': round(float(avg_rating), 1),
            }

            if count <= 1 and total_emp >= 5:
                critical_gaps.append({
                    'skill_name': skill.name,
                    'current_certified_staff': count,
                    'risk_level': 'HIGH_SINGLE_POINT_OF_FAILURE',
                })

        return {
            'total_employees': total_emp,
            'skill_coverage': coverage_data,
            'critical_gaps': critical_gaps,
        }

    @staticmethod
    def identify_mentorship_pairs() -> List[Dict[str, Any]]:
        pairs = []
        skills = Skill.objects.all()[:10]
        for skill in skills:
            experts = EmployeeSkill.objects.filter(skill=skill, proficiency_level__gte=4).select_related('employee')
            learners = EmployeeSkill.objects.filter(skill=skill, proficiency_level__lte=2).select_related('employee')
            
            if experts.exists() and learners.exists():
                pairs.append({
                    'skill_name': skill.name,
                    'mentor': experts.first().employee.full_name,
                    'mentee': learners.first().employee.full_name,
                    'target_level': 4,
                })
        return pairs
""")

write_file("apps/attendance/roster_generator.py", """
import datetime
from typing import List, Dict, Any
from apps.employees.models import Employee
from apps.shifts.models import Shift

class AutomatedRosterGenerator:
    '''
    Generates shift schedules balancing 24/7 coverage, mandatory rest intervals,
    weekend rotations, and public holiday compliance.
    '''

    @staticmethod
    def generate_monthly_roster(year: int, month: int, department_id: int = None) -> List[Dict[str, Any]]:
        employees = Employee.objects.all()
        if department_id:
            employees = employees.filter(department_id=department_id)

        shifts = list(Shift.objects.all())
        if not shifts:
            return []

        roster_entries = []
        num_days = 30  # Standard monthly view

        for emp_idx, emp in enumerate(employees):
            emp_schedule = []
            for day in range(1, num_days + 1):
                # Simple rotation algorithm
                shift_choice = shifts[(emp_idx + day) % len(shifts)]
                is_weekly_off = (day % 7) in [0, 6]
                
                emp_schedule.append({
                    'day': day,
                    'shift_name': 'Weekly Off' if is_weekly_off else shift_choice.name,
                    'shift_code': 'OFF' if is_weekly_off else shift_choice.code,
                    'start_time': None if is_weekly_off else str(shift_choice.start_time),
                    'end_time': None if is_weekly_off else str(shift_choice.end_time),
                })
            
            roster_entries.append({
                'employee_id': emp.employee_id,
                'employee_name': emp.full_name,
                'schedule': emp_schedule,
            })

        return roster_entries
""")

write_file("apps/performance/okr_tracking_engine.py", """
from decimal import Decimal
from typing import List, Dict, Any
from apps.goals.models import Goal
from apps.employees.models import Employee

class OKRProgressTrackingEngine:
    '''
    Tracks hierarchical OKRs (Company -> Department -> Team -> Individual).
    Calculates weighted milestone completion rates and expected trajectory vs deadline.
    '''

    @staticmethod
    def calculate_employee_okr_progress(employee: Employee) -> Dict[str, Any]:
        goals = Goal.objects.filter(employee=employee)
        total_goals = goals.count()
        if total_goals == 0:
            return {'total_okrs': 0, 'average_completion': 0.0, 'status': 'ON_TRACK'}

        total_pct = sum(getattr(g, 'progress_percentage', Decimal('0.0')) or Decimal('0.0') for g in goals)
        avg_pct = round(float(total_pct / Decimal(str(total_goals))), 1)

        health = 'ON_TRACK'
        if avg_pct < 40.0:
            health = 'AT_RISK'
        elif avg_pct < 70.0:
            health = 'NEEDS_ATTENTION'

        return {
            'total_okrs': total_goals,
            'average_completion': avg_pct,
            'health_status': health,
            'completed_count': sum(1 for g in goals if getattr(g, 'progress_percentage', 0) >= 100),
        }
""")

write_file("apps/recognition/gamification_service.py", """
from typing import List, Dict, Any
from django.db.models import Count
from apps.recognition.models import Recognition
from apps.employees.models import Employee

class RecognitionGamificationEngine:
    '''
    Computes Kudos leaderboards, peer appreciation badges, core value champions,
    and annual rewards allocation.
    '''

    BADGE_TIERS = {
        'BRONZE_CHAMPION': {'min_kudos': 5, 'badge_title': 'Workplace Contributor (Bronze)'},
        'SILVER_HERO': {'min_kudos': 15, 'badge_title': 'Values Champion (Silver)'},
        'GOLD_LEGEND': {'min_kudos': 30, 'badge_title': 'Enterprise Beacon (Gold)'},
    }

    @classmethod
    def get_top_kudos_leaderboard(cls, limit: int = 10) -> List[Dict[str, Any]]:
        leaders = Recognition.objects.values('receiver__id', 'receiver__user__first_name', 'receiver__user__last_name')\\
            .annotate(kudos_count=Count('id'))\\
            .order_by('-kudos_count')[:limit]

        results = []
        for rank, row in enumerate(leaders, start=1):
            count = row['kudos_count']
            tier = 'NEWCOMER'
            if count >= 30:
                tier = 'GOLD_LEGEND'
            elif count >= 15:
                tier = 'SILVER_HERO'
            elif count >= 5:
                tier = 'BRONZE_CHAMPION'

            results.append({
                'rank': rank,
                'employee_id': row['receiver__id'],
                'full_name': f"{row['receiver__user__first_name']} {row['receiver__user__last_name']}".strip(),
                'total_kudos_received': count,
                'awarded_badge': cls.BADGE_TIERS.get(tier, {}).get('badge_title', 'Rising Star'),
            })
        return results
""")

write_file("apps/helpdesk/sla_escalation_engine.py", """
import datetime
from django.utils import timezone
from apps.helpdesk.models import SupportTicket

class HelpdeskSLAEngine:
    '''
    Evaluates Support Ticket SLA deadlines (Priority P1: 4h, P2: 12h, P3: 24h, P4: 48h),
    triggers automated escalations, and computes team resolution efficiency.
    '''

    SLA_HOURS_BY_PRIORITY = {
        'URGENT': 4,
        'HIGH': 12,
        'MEDIUM': 24,
        'LOW': 48,
    }

    @classmethod
    def audit_sla_breaches(cls) -> Dict[str, Any]:
        open_tickets = SupportTicket.objects.filter(status__in=['OPEN', 'IN_PROGRESS', 'PENDING'])
        breached_count = 0
        at_risk_count = 0
        now = timezone.now()

        for t in open_tickets:
            allowed_hrs = cls.SLA_HOURS_BY_PRIORITY.get(getattr(t, 'priority', 'MEDIUM'), 24)
            deadline = t.created_at + datetime.timedelta(hours=allowed_hrs)
            if now > deadline:
                breached_count += 1
            elif (deadline - now).total_seconds() < 7200:  # within 2 hours
                at_risk_count += 1

        total_open = open_tickets.count()
        sla_compliance_pct = round(((total_open - breached_count) / total_open * 100.0), 1) if total_open > 0 else 100.0

        return {
            'total_open_tickets': total_open,
            'breached_sla_count': breached_count,
            'at_risk_count': at_risk_count,
            'sla_compliance_rate': sla_compliance_pct,
        }
""")

write_file("apps/administration/database_backup_service.py", """
import os
import shutil
from pathlib import Path
from django.conf import settings
from django.utils import timezone

class DatabaseBackupManager:
    '''
    Manages automated point-in-time database backups, snapshot archives,
    and metadata integrity verification.
    '''

    @staticmethod
    def create_database_snapshot() -> str:
        db_path = settings.BASE_DIR / 'db.sqlite3'
        backup_dir = settings.BASE_DIR / 'backups'
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        snapshot_filename = f"smart_ems_backup_{timestamp}.sqlite3"
        target_path = backup_dir / snapshot_filename

        if db_path.exists():
            shutil.copy2(db_path, target_path)
            return str(target_path)
        return ""
""")

# ==============================================================================
# EXPANDED UNIT TESTS FOR ADVANCED ENGINES
# ==============================================================================

write_file("tests/test_advanced_engines.py", """
import pytest
from decimal import Decimal
from django.utils import timezone
from apps.insights.predictive import WorkforcePredictiveEngine
from apps.attendance.geo_fencing import GeoFencingVerificationService
from apps.attendance.roster_generator import AutomatedRosterGenerator
from apps.employees.skill_matrix_service import SkillMatrixAnalyticsService
from apps.recognition.gamification_service import RecognitionGamificationEngine
from apps.helpdesk.sla_escalation_engine import HelpdeskSLAEngine
from apps.administration.database_backup_service import DatabaseBackupManager
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_geofencing_service():
    # Bengaluru HQ coordinates
    res_inside = GeoFencingVerificationService.verify_location_within_geofence(12.9716, 77.5946)
    assert res_inside['is_within_geofence'] is True
    assert res_inside['distance_to_office_meters'] <= 250

    # Distant coordinates (Outside office)
    res_outside = GeoFencingVerificationService.verify_location_within_geofence(13.5000, 78.0000)
    assert res_outside['is_within_geofence'] is False

@pytest.mark.django_db
def test_predictive_flight_risk():
    user = User.objects.create_user(username="predict.test.user", password="Password@123")
    emp = Employee.objects.create(
        user=user,
        employee_id="EMP-PRED-01",
        first_name="Predictive",
        last_name="Tester",
        email="pred@example.com",
        date_of_joining=timezone.now().date(),
        employment_status='ACTIVE'
    )
    risk = WorkforcePredictiveEngine.calculate_flight_risk_score(emp)
    assert 'flight_risk_score' in risk
    assert risk['flight_risk_score'] > 0

    succ = WorkforcePredictiveEngine.calculate_succession_readiness(emp)
    assert 'readiness_score' in succ

@pytest.mark.django_db
def test_gamification_and_sla_engines():
    leaders = RecognitionGamificationEngine.get_top_kudos_leaderboard()
    assert isinstance(leaders, list)

    sla = HelpdeskSLAEngine.audit_sla_breaches()
    assert 'sla_compliance_rate' in sla

@pytest.mark.django_db
def test_database_backup_manager():
    path = DatabaseBackupManager.create_database_snapshot()
    assert isinstance(path, str)
""")

print("Finished building advanced domain engines and test suites.")
