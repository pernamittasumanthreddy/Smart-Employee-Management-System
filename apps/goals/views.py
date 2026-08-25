from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.goals.forms import GoalForm, GoalProgressUpdateForm
from apps.goals.models import Goal, GoalStatus
from apps.permissions.decorators import manager_or_above_required


@login_required
def goal_list_view(request):
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status')
    
    goals = Goal.objects.all().select_related('employee', 'team')
    if search:
        goals = goals.filter(Q(title__icontains=search) | Q(employee__first_name__icontains=search))
    if status:
        goals = goals.filter(status=status)

    total_goals = goals.count()
    achieved = goals.filter(status=GoalStatus.ACHIEVED).count()
    in_progress = goals.filter(status=GoalStatus.IN_PROGRESS).count()
    avg_progress = goals.aggregate(avg=Avg('progress_percentage'))['avg'] or 0

    return render(request, 'goals/goal_list.html', {
        'goals': goals,
        'search': search,
        'selected_status': status,
        'total_goals': total_goals,
        'achieved': achieved,
        'in_progress': in_progress,
        'avg_progress': round(avg_progress, 1)
    })

@login_required
def my_goals_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    goals = Goal.objects.filter(Q(employee=employee) | Q(team=employee.team)).distinct()
    return render(request, 'goals/my_goals.html', {'goals': goals})

@login_required
@manager_or_above_required
def goal_create_view(request):
    form = GoalForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        goal = form.save(commit=False)
        current_emp = getattr(request.user, 'employee_profile', None)
        goal.created_by = current_emp
        goal.save()
        messages.success(request, f"Goal '{goal.title}' created.")
        return redirect('goals:goal_list')
    return render(request, 'goals/goal_form.html', {'form': form, 'title': 'Create New Goal'})

@login_required
def goal_detail_view(request, goal_id):
    goal = get_object_or_404(Goal.objects.select_related('employee', 'team', 'created_by'), id=goal_id)
    form = GoalProgressUpdateForm(initial={'progress_percentage': goal.progress_percentage, 'current_value': goal.current_value})
    
    if request.method == 'POST':
        form = GoalProgressUpdateForm(request.POST)
        if form.is_valid():
            goal.progress_percentage = form.cleaned_data['progress_percentage']
            if form.cleaned_data['current_value'] is not None:
                goal.current_value = form.cleaned_data['current_value']
            if goal.progress_percentage >= 100:
                goal.status = GoalStatus.ACHIEVED
            goal.save()
            messages.success(request, "Goal progress updated.")
            return redirect('goals:goal_detail', goal_id=goal.id)

    return render(request, 'goals/goal_detail.html', {'goal': goal, 'form': form})
