from django.contrib import admin
from apps.automation.models import AutomationRule, ExecutionLog

@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'trigger_event', 'action_type', 'is_active', 'total_executions')

@admin.register(ExecutionLog)
class ExecutionLogAdmin(admin.ModelAdmin):
    list_display = ('rule', 'executed_at', 'status')
    list_filter = ('status',)
