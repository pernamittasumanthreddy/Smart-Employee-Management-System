from django.urls import path

from apps.administration import views

app_name = 'administration'

urlpatterns = [
    path('audit-logs/', views.audit_logs_list_view, name='audit_logs'),
    path('audit-logs/export/', views.export_audit_logs_csv, name='export_audit_logs'),
    path('security-compliance/', views.security_compliance_view, name='security_compliance'),
    path('settings/', views.system_settings_view, name='settings'),
    path('backups/', views.backup_dashboard_view, name='backups'),
    path('backups/trigger/', views.trigger_backup_action, name='trigger_backup'),
]
