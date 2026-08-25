import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.assets.models import Asset
from apps.expenses.models import ExpenseClaim
from apps.organization.models import Department
from apps.performance.models import ReviewCycle
from apps.permissions.decorators import manager_or_above_required
from apps.projects.models import Project
from apps.reports.services import ReportAnalyticsService
from apps.skills.models import Skill
from apps.tasks.models import Task
from apps.training.models import Course, TrainingEnrollment


@login_required
@manager_or_above_required
def reports_hub_view(request):
    """
    Centralized outputs & reports directory.
    """
    overview = ReportAnalyticsService.get_executive_overview()
    return render(request, 'reports/hub.html', overview)

@login_required
@manager_or_above_required
def attendance_leave_report_view(request):
    dept_id = request.GET.get('department')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    data = ReportAnalyticsService.get_attendance_leave_report_data(start_date, end_date, dept_id)
    departments = Department.objects.filter(is_active=True)

    return render(request, 'reports/attendance_leave_report.html', {
        'data': data,
        'departments': departments,
        'selected_dept': dept_id,
        'start_date': start_date,
        'end_date': end_date,
    })

@login_required
@manager_or_above_required
def performance_analytics_view(request):
    cycle_id = request.GET.get('cycle')
    dept_id = request.GET.get('department')

    data = ReportAnalyticsService.get_performance_analytics_data(cycle_id, dept_id)
    cycles = ReviewCycle.objects.all()
    departments = Department.objects.filter(is_active=True)

    return render(request, 'reports/performance_analytics.html', {
        'data': data,
        'cycles': cycles,
        'departments': departments,
        'selected_cycle': cycle_id,
        'selected_dept': dept_id,
    })

@login_required
@manager_or_above_required
def project_task_tracking_view(request):
    projects = Project.objects.all().prefetch_related('tasks')
    tasks = Task.objects.all().select_related('project', 'assigned_to')

    status_dist = {
        'TODO': tasks.filter(status='TODO').count(),
        'IN_PROGRESS': tasks.filter(status='IN_PROGRESS').count(),
        'REVIEW': tasks.filter(status='REVIEW').count(),
        'COMPLETED': tasks.filter(status='COMPLETED').count(),
    }

    priority_dist = {
        'URGENT': tasks.filter(priority='URGENT').count(),
        'HIGH': tasks.filter(priority='HIGH').count(),
        'MEDIUM': tasks.filter(priority='MEDIUM').count(),
        'LOW': tasks.filter(priority='LOW').count(),
    }

    return render(request, 'reports/project_task_tracking.html', {
        'projects': projects,
        'tasks': tasks[:50],
        'status_labels_json': json.dumps(list(status_dist.keys())),
        'status_data_json': json.dumps(list(status_dist.values())),
        'priority_labels_json': json.dumps(list(priority_dist.keys())),
        'priority_data_json': json.dumps(list(priority_dist.values())),
    })

@login_required
@manager_or_above_required
def skill_training_insights_view(request):
    skills = Skill.objects.all().select_related('category').prefetch_related('employee_skills')
    courses = Course.objects.all().prefetch_related('enrollments')

    completed_enrollments = TrainingEnrollment.objects.filter(status='COMPLETED').count()
    active_enrollments = TrainingEnrollment.objects.filter(status__in=['ENROLLED', 'IN_PROGRESS']).count()

    return render(request, 'reports/skill_training_insights.html', {
        'skills': skills,
        'courses': courses,
        'completed_enrollments': completed_enrollments,
        'active_enrollments': active_enrollments,
    })

@login_required
@manager_or_above_required
def expense_asset_tracking_view(request):
    assets = Asset.objects.all().select_related('category', 'assigned_to')
    expenses = ExpenseClaim.objects.all().select_related('category', 'employee')

    asset_status_counts = {
        'AVAILABLE': assets.filter(status='AVAILABLE').count(),
        'ASSIGNED': assets.filter(status='ASSIGNED').count(),
        'MAINTENANCE': assets.filter(status='MAINTENANCE').count(),
        'RETIRED': assets.filter(status='RETIRED').count(),
    }

    expense_status_counts = {
        'PENDING': expenses.filter(status='PENDING').count(),
        'APPROVED': expenses.filter(status='APPROVED').count(),
        'REIMBURSED': expenses.filter(status='REIMBURSED').count(),
        'REJECTED': expenses.filter(status='REJECTED').count(),
    }

    return render(request, 'reports/expense_asset_tracking.html', {
        'assets': assets[:30],
        'expenses': expenses[:30],
        'asset_labels_json': json.dumps(list(asset_status_counts.keys())),
        'asset_data_json': json.dumps(list(asset_status_counts.values())),
        'expense_labels_json': json.dumps(list(expense_status_counts.keys())),
        'expense_data_json': json.dumps(list(expense_status_counts.values())),
    })
