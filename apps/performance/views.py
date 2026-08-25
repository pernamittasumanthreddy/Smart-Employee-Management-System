from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import redirect, render

from apps.performance.forms import PerformanceEvaluationForm, ReviewCycleForm
from apps.performance.models import PerformanceEvaluation, ReviewCycle
from apps.permissions.decorators import manager_or_above_required


@login_required
@manager_or_above_required
def evaluations_list_view(request):
    cycle_id = request.GET.get('cycle')
    dept_id = request.GET.get('department')

    evaluations = PerformanceEvaluation.objects.all().select_related('employee__department', 'cycle', 'evaluator')

    if cycle_id:
        evaluations = evaluations.filter(cycle_id=cycle_id)
    if dept_id:
        evaluations = evaluations.filter(employee__department_id=dept_id)

    cycles = ReviewCycle.objects.all()
    avg_score = evaluations.aggregate(avg=Avg('final_score'))['avg'] or 0.0

    return render(request, 'performance/evaluation_list.html', {
        'evaluations': evaluations,
        'cycles': cycles,
        'selected_cycle': cycle_id,
        'avg_score': round(avg_score, 2),
    })

@login_required
def my_performance_reviews_view(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required.")
        return redirect('authentication:dashboard')

    reviews = PerformanceEvaluation.objects.filter(employee=employee).select_related('cycle', 'evaluator')
    return render(request, 'performance/my_reviews.html', {'reviews': reviews})

@login_required
@manager_or_above_required
def conduct_evaluation_view(request):
    form = PerformanceEvaluationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        eval_obj = form.save(commit=False)
        evaluator_emp = getattr(request.user, 'employee_profile', None)
        eval_obj.evaluator = evaluator_emp
        eval_obj.calculate_final_score()
        eval_obj.save()
        messages.success(request, f"Performance review for {eval_obj.employee.full_name} submitted successfully (Score: {eval_obj.final_score}/5.0).")
        return redirect('performance:evaluation_list')
    return render(request, 'performance/evaluation_form.html', {'form': form, 'title': 'Conduct Employee Performance Evaluation'})

@login_required
@manager_or_above_required
def cycle_list_view(request):
    cycles = ReviewCycle.objects.all().prefetch_related('evaluations')
    form = ReviewCycleForm(request.POST or None)
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.role in ('ADMIN', 'HR')):
            messages.error(request, "Only HR managers and administrators can create review cycles.")
            return redirect('performance:cycle_list')
        if form.is_valid():
            c = form.save()
            messages.success(request, f"Review cycle '{c.title}' created.")
            return redirect('performance:cycle_list')
    return render(request, 'performance/cycle_list.html', {'cycles': cycles, 'form': form})
