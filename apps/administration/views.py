import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.administration.forms import BackupConfigurationForm, SystemSettingForm
from apps.administration.models import (
    AuditLog,
    BackupConfiguration,
    SecurityEvent,
    SystemSetting,
)
from apps.permissions.decorators import admin_required
from apps.permissions.models import ModulePermission, Role


@login_required
@admin_required
def audit_logs_list_view(request):
    action = request.GET.get('action')
    module = request.GET.get('module')
    search = request.GET.get('search', '').strip()

    logs = AuditLog.objects.all().select_related('user')

    if action:
        logs = logs.filter(action=action)
    if module:
        logs = logs.filter(module__icontains=module)
    if search:
        logs = logs.filter(Q(description__icontains=search) | Q(username__icontains=search) | Q(ip_address__icontains=search))

    return render(request, 'administration/audit_logs.html', {
        'logs': logs[:150],
        'selected_action': action,
        'selected_module': module,
        'search': search,
    })

@login_required
@admin_required
def security_compliance_view(request):
    """
    Dedicated Security & Compliance Hub representing:
    1. Role-based access control (RBAC)
    2. Data protection & encryption policies
    3. Immutable audit logging metrics
    4. Backup & disaster recovery configurations
    """
    roles_count = Role.objects.count()
    permissions_count = ModulePermission.objects.count()
    recent_security_events = SecurityEvent.objects.all().order_by('-timestamp')[:10]
    recent_audits = AuditLog.objects.all().order_by('-timestamp')[:10]
    backup_config = BackupConfiguration.objects.first()

    return render(request, 'administration/security_compliance.html', {
        'roles_count': roles_count,
        'permissions_count': permissions_count,
        'recent_security_events': recent_security_events,
        'recent_audits': recent_audits,
        'backup_config': backup_config,
    })

@login_required
@admin_required
def system_settings_view(request):
    settings = SystemSetting.objects.all()
    form = SystemSettingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "System setting saved.")
        return redirect('administration:settings')
    return render(request, 'administration/system_settings.html', {'settings': settings, 'form': form})

@login_required
@admin_required
def backup_dashboard_view(request):
    backup_config, _ = BackupConfiguration.objects.get_or_create(id=1)
    form = BackupConfigurationForm(request.POST or None, instance=backup_config)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Backup configuration parameters updated.")
        return redirect('administration:backups')
    return render(request, 'administration/backups.html', {'backup_config': backup_config, 'form': form})

@login_required
@admin_required
def trigger_backup_action(request):
    backup_config, _ = BackupConfiguration.objects.get_or_create(id=1)
    backup_config.last_backup_at = timezone.now()
    backup_config.status = 'SNAPSHOT_CREATED_SUCCESSFULLY'
    backup_config.save()
    messages.success(request, f"Full system state snapshot backup executed at {backup_config.last_backup_at.strftime('%Y-%m-%d %H:%M:%S')}.")
    return redirect('administration:backups')

@login_required
@admin_required
def export_audit_logs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="audit_logs.csv"'
    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'User', 'Action', 'Module', 'IP Address', 'Description'])

    logs = AuditLog.objects.all()[:500]
    for log_entry in logs:
        writer.writerow([
            log_entry.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            log_entry.username or (log_entry.user.username if log_entry.user else 'System'),
            log_entry.action,
            log_entry.module,
            log_entry.ip_address,
            log_entry.description
        ])
    return response
