import pytest
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
