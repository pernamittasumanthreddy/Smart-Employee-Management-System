from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import redirect, render

from apps.organization.models import Department
from apps.permissions.decorators import manager_or_above_required
from apps.workload.models import EmployeeWorkloadMetric, UtilizationStatus
from apps.workload.services import WorkloadCalculationService


@login_required
@manager_or_above_required
def workload_dashboard_view(request):
    dept_id = request.GET.get('department')
    status_filter = request.GET.get('status')

    metrics = EmployeeWorkloadMetric.objects.all().select_related(
        'employee__department', 'employee__designation', 'employee__team'
    )

    if dept_id:
        metrics = metrics.filter(employee__department_id=dept_id)
    if status_filter:
        metrics = metrics.filter(utilization_status=status_filter)

    # Overview statistics
    total_tracked = metrics.count()
    overloaded_count = metrics.filter(utilization_status=UtilizationStatus.OVERLOADED).count()
    underutilized_count = metrics.filter(utilization_status=UtilizationStatus.UNDERUTILIZED).count()
    optimal_count = metrics.filter(utilization_status__in=[UtilizationStatus.BALANCED, UtilizationStatus.OPTIMAL]).count()
    avg_score = metrics.aggregate(avg=Avg('workload_score'))['avg'] or 0

    departments = Department.objects.filter(is_active=True)

    return render(request, 'workload/dashboard.html', {
        'metrics': metrics,
        'departments': departments,
        'selected_dept': dept_id,
        'selected_status': status_filter,
        'total_tracked': total_tracked,
        'overloaded_count': overloaded_count,
        'underutilized_count': underutilized_count,
        'optimal_count': optimal_count,
        'avg_score': round(avg_score, 1),
    })

@login_required
@manager_or_above_required
def recalculate_workload_action(request):
    WorkloadCalculationService.recalculate_all()
    messages.success(request, "Employee workload metrics successfully recalculated across all active workforce members.")
    return redirect('workload:dashboard')
