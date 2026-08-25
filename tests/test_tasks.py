import pytest
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
