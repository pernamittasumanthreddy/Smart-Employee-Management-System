import pytest
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
