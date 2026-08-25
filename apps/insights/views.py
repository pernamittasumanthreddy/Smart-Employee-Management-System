from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.insights.insight_service import SmartInsightService
from apps.insights.models import InsightCategory, InsightSeverity, SmartInsight
from apps.organization.models import Department
from apps.permissions.decorators import manager_or_above_required


@login_required
@manager_or_above_required
def smart_insights_dashboard_view(request):
    category = request.GET.get('category')
    severity = request.GET.get('severity')
    dept_id = request.GET.get('department')

    insights = SmartInsight.objects.filter(is_dismissed=False).select_related('employee__department', 'department')

    if category:
        insights = insights.filter(category=category)
    if severity:
        insights = insights.filter(severity=severity)
    if dept_id:
        insights = insights.filter(Q(department_id=dept_id) | Q(employee__department_id=dept_id))

    total_count = insights.count()
    high_priority = insights.filter(severity=InsightSeverity.HIGH).count()
    medium_priority = insights.filter(severity=InsightSeverity.MEDIUM).count()
    positive_trends = insights.filter(severity=InsightSeverity.POSITIVE).count()

    categories = InsightCategory.choices
    severities = InsightSeverity.choices
    departments = Department.objects.filter(is_active=True)

    return render(request, 'insights/dashboard.html', {
        'insights': insights,
        'categories': categories,
        'severities': severities,
        'departments': departments,
        'selected_category': category,
        'selected_severity': severity,
        'selected_dept': dept_id,
        'total_count': total_count,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'positive_trends': positive_trends,
    })

@login_required
@manager_or_above_required
def trigger_analysis_action(request):
    count = SmartInsightService.run_full_system_analysis()
    messages.success(request, f"Intelligence engine execution complete. Generated {count} explainable actionable insights.")
    return redirect('insights:dashboard')

@login_required
@manager_or_above_required
def dismiss_insight_action(request, insight_id):
    insight = get_object_or_404(SmartInsight, id=insight_id)
    insight.is_dismissed = True
    insight.save()
    messages.info(request, "Insight marked as reviewed and dismissed.")
    return redirect('insights:dashboard')
