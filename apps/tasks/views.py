from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.notifications.services import NotificationService
from apps.permissions.decorators import manager_or_above_required
from apps.projects.models import Project
from apps.tasks.forms import SubTaskForm, TaskCommentForm, TaskForm
from apps.tasks.models import SubTask, Task, TaskStatus
from apps.workload.services import WorkloadCalculationService


@login_required
def task_list_view(request):
    search = request.GET.get('search', '').strip()
    proj_id = request.GET.get('project')
    priority = request.GET.get('priority')
    status = request.GET.get('status')
    assignee_id = request.GET.get('assigned_to')

    tasks = Task.objects.all().select_related('project', 'assigned_to', 'created_by')

    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(code__icontains=search))
    if proj_id:
        tasks = tasks.filter(project_id=proj_id)
    if priority:
        tasks = tasks.filter(priority=priority)
    if status:
        tasks = tasks.filter(status=status)
    if assignee_id:
        tasks = tasks.filter(assigned_to_id=assignee_id)

    projects = Project.objects.filter(status='ACTIVE')
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'projects': projects,
        'selected_proj': proj_id,
        'selected_priority': priority,
        'selected_status': status,
        'search': search,
    })

@login_required
def my_tasks_kanban(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    tasks = Task.objects.filter(assigned_to=employee).select_related('project')
    
    todo_tasks = tasks.filter(status=TaskStatus.TODO)
    inprogress_tasks = tasks.filter(status=TaskStatus.IN_PROGRESS)
    review_tasks = tasks.filter(status=TaskStatus.REVIEW)
    completed_tasks = tasks.filter(status=TaskStatus.COMPLETED)

    return render(request, 'tasks/kanban.html', {
        'todo_tasks': todo_tasks,
        'inprogress_tasks': inprogress_tasks,
        'review_tasks': review_tasks,
        'completed_tasks': completed_tasks,
    })

@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related('project', 'assigned_to', 'created_by').prefetch_related('subtasks', 'comments__author'),
        id=task_id
    )
    comment_form = TaskCommentForm()
    subtask_form = SubTaskForm()

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'subtasks': task.subtasks.all(),
        'comments': task.comments.all(),
        'comment_form': comment_form,
        'subtask_form': subtask_form,
    })

@login_required
@manager_or_above_required
def task_create_view(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        current_emp = getattr(request.user, 'employee_profile', None)
        task.created_by = current_emp
        task.save()
        
        # Trigger project progress rollup & employee workload update
        task.project.recalculate_progress()
        if task.assigned_to:
            WorkloadCalculationService.calculate_for_employee(task.assigned_to)
            if task.assigned_to.user:
                NotificationService.create_notification(
                    user=task.assigned_to.user,
                    title="New Task Assigned",
                    message=f"You have been assigned task [{task.code}] {task.title}.",
                    category='TASK',
                    link=f"/tasks/{task.id}/"
                )

        messages.success(request, f"Task '{task.title}' created.")
        return redirect('tasks:task_detail', task_id=task.id)

    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create New Task'})

@login_required
def task_update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    new_status = request.POST.get('status')
    if new_status in TaskStatus.values:
        task.status = new_status
        if new_status == TaskStatus.COMPLETED:
            task.completion_date = timezone.now().date()
        task.save()
        task.project.recalculate_progress()
        if task.assigned_to:
            WorkloadCalculationService.calculate_for_employee(task.assigned_to)
        messages.success(request, f"Task status updated to {task.get_status_display()}.")
    return redirect('tasks:task_detail', task_id=task.id)

@login_required
def task_add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    author = getattr(request.user, 'employee_profile', None)
    if request.method == 'POST' and author:
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = author
            comment.save()
            messages.success(request, "Comment posted.")
    return redirect('tasks:task_detail', task_id=task.id)

@login_required
def task_add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.task = task
            sub.save()
            messages.success(request, "Subtask added.")
    return redirect('tasks:task_detail', task_id=task.id)

@login_required
def task_toggle_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    subtask.is_completed = not subtask.is_completed
    subtask.save()
    return redirect('tasks:task_detail', task_id=subtask.task.id)
