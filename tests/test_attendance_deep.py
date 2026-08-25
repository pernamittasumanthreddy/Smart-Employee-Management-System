import pytest
from decimal import Decimal
from django.utils import timezone
from apps.attendance.models import AttendanceRecord
from apps.attendance.geo_fencing import GeoFencingVerificationService
from apps.attendance.roster_generator import AutomatedRosterGenerator
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestAttendanceDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="attn.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-ATTN-DEEP-01",
            first_name="Pooja",
            last_name="Hegde",
            email="pooja.attn@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )

    def test_daily_punch_record(self):
        rec = AttendanceRecord.objects.create(
            employee=self.emp,
            date=timezone.now().date(),
            status='PRESENT',
            check_in_time=timezone.now(),
            check_out_time=timezone.now()
        )
        assert rec.status == 'PRESENT'
        assert rec.employee == self.emp

    def test_geofence_haversine_formula(self):
        res = GeoFencingVerificationService.verify_location_within_geofence(12.9716, 77.5946)
        assert res['is_within_geofence'] is True

    def test_roster_generator(self):
        roster = AutomatedRosterGenerator.generate_monthly_roster(2026, 8)
        assert isinstance(roster, list)
