from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.automation.models import AutomationRule, ExecutionLog

@login_required
def automation_dashboard(request):
    rules = AutomationRule.objects.all()
    logs = ExecutionLog.objects.select_related('rule')[:15]
    active_count = rules.filter(is_active=True).count()
    total_runs = sum(r.total_executions for r in rules)

    context = {
        'rules': rules,
        'logs': logs,
        'active_count': active_count,
        'total_runs': total_runs,
    }
    return render(request, 'automation/dashboard.html', context)

@login_required
def trigger_rule_simulation(request, pk):
    rule = get_object_or_404(AutomationRule, pk=pk)
    rule.total_executions += 1
    rule.save()
    ExecutionLog.objects.create(
        rule=rule,
        status='SUCCESS',
        details=f"Automated workflow trigger simulation succeeded for rule '{rule.name}' with event {rule.trigger_event}."
    )
    messages.success(request, f"Rule '{rule.name}' executed successfully!")
    return redirect('automation:dashboard')
