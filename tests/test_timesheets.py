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
