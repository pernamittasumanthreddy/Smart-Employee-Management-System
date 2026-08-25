import pytest
from decimal import Decimal
from django.utils import timezone
from apps.tasks.models import Task, Subtask
from apps.projects.models import Project
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestTasksDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="task.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-TASK-DEEP-01",
            first_name="Shreya",
            last_name="Ghoshal",
            email="shreya.task@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.proj = Project.objects.create(
            name="Infrastructure Modernization",
            code="PRJ-INFRA-01",
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )

    def test_task_lifecycle_and_subtasks(self):
        t = Task.objects.create(
            project=self.proj,
            title="Configure Terraform Kubernetes Cluster",
            assigned_to=self.emp,
            priority="HIGH",
            status="IN_PROGRESS",
            estimated_hours=Decimal('16.0'),
            due_date=timezone.now().date()
        )
        sub1 = Subtask.objects.create(task=t, title="VPC & Subnets Setup", is_completed=True)
        sub2 = Subtask.objects.create(task=t, title="IAM Role Least Privilege Setup", is_completed=True)
        assert t.subtasks.count() == 2
        assert sub1.is_completed is True
