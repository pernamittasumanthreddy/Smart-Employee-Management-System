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
