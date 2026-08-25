import pytest
from decimal import Decimal
from django.utils import timezone
from apps.projects.models import Project, Milestone
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestProjectsDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="proj.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-PROJ-DEEP-01",
            first_name="Karan",
            last_name="Johar",
            email="karan.proj@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.proj = Project.objects.create(
            name="Enterprise Core Platform 3.0",
            code="PRJ-CORE-30",
            manager=self.emp,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            status="IN_PROGRESS",
            budget=Decimal('5000000.00'),
            progress_percentage=65
        )

    def test_project_properties(self):
        assert self.proj.code == "PRJ-CORE-30"
        assert self.proj.budget == Decimal('5000000.00')
        assert self.proj.progress_percentage == 65

    def test_milestone_creation(self):
        m = Milestone.objects.create(
            project=self.proj,
            title="Database Sharding & Microservices V1",
            due_date=timezone.now().date(),
            is_completed=True
        )
        assert m.project == self.proj
        assert m.is_completed is True
