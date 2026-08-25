import pytest
from decimal import Decimal
from django.utils import timezone
from apps.timesheets.models import ProjectRateCard, WeeklyTimesheet, TimesheetEntry
from apps.projects.models import Project
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestTimesheetsDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="ts.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-TS-DEEP-01",
            first_name="Rohan",
            last_name="Gavaskar",
            email="rohan.ts@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.proj = Project.objects.create(
            name="Fintech Core Banking Integration",
            code="PRJ-FIN-01",
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )
        self.rate = ProjectRateCard.objects.create(
            project=self.proj,
            role_name="Lead Cloud Solutions Architect",
            hourly_billing_rate=Decimal('120.00'),
            currency="USD"
        )

    def test_timesheet_entry_and_totals(self):
        ts = WeeklyTimesheet.objects.create(
            employee=self.emp,
            week_start_date=timezone.now().date(),
            week_end_date=timezone.now().date(),
            total_billable_hours=Decimal('32.00'),
            total_non_billable_hours=Decimal('8.00'),
            status="APPROVED"
        )
        entry = TimesheetEntry.objects.create(
            timesheet=ts,
            project=self.proj,
            date=timezone.now().date(),
            hours=Decimal('8.00'),
            is_billable=True,
            task_description="Architectural Review & Kubernetes Deployment"
        )
        assert ts.total_hours == Decimal('40.00')
        assert entry.is_billable is True
        assert self.rate.hourly_billing_rate == Decimal('120.00')
