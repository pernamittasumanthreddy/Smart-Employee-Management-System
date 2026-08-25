from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.permissions.decorators import manager_or_above_required
from apps.projects.forms import ProjectForm, ProjectMilestoneForm
from apps.projects.models import Project, ProjectMilestone, ProjectStatus


@login_required
def project_list_view(request):
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status')
    
    projects = Project.objects.all().select_related('manager').prefetch_related('members')
    
    if search:
        projects = projects.filter(Q(name__icontains=search) | Q(code__icontains=search))
    if status:
        projects = projects.filter(status=status)

    total_projects = projects.count()
    active_projects = projects.filter(status=ProjectStatus.ACTIVE).count()
    completed_projects = projects.filter(status=ProjectStatus.COMPLETED).count()

    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'search': search,
        'selected_status': status,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
    })

@login_required
def project_detail_view(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related('manager').prefetch_related('members', 'milestones', 'tasks__assigned_to'),
        id=project_id
    )
    milestone_form = ProjectMilestoneForm()
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'milestones': project.milestones.all(),
        'tasks': project.tasks.all(),
        'milestone_form': milestone_form,
    })

@login_required
@manager_or_above_required
def project_create_view(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        project = form.save()
        messages.success(request, f"Project '{project.name}' initialized.")
        return redirect('projects:project_detail', project_id=project.id)
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Create New Project'})

@login_required
@manager_or_above_required
def project_update_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == 'POST' and form.is_valid():
        form.save()
        project.recalculate_progress()
        messages.success(request, f"Project '{project.name}' updated.")
        return redirect('projects:project_detail', project_id=project.id)
    return render(request, 'projects/project_form.html', {'form': form, 'title': f'Edit Project - {project.name}'})

@login_required
@manager_or_above_required
def project_add_milestone(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectMilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.project = project
            milestone.save()
            messages.success(request, f"Milestone '{milestone.title}' added.")
    return redirect('projects:project_detail', project_id=project.id)

@login_required
@manager_or_above_required
def project_toggle_milestone(request, milestone_id):
    milestone = get_object_or_404(ProjectMilestone, id=milestone_id)
    milestone.is_completed = not milestone.is_completed
    milestone.completion_date = timezone.now().date() if milestone.is_completed else None
    milestone.save()
    messages.success(request, f"Milestone '{milestone.title}' status updated.")
    return redirect('projects:project_detail', project_id=milestone.project.id)
