from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.compliance.models import StatutoryRegister, ComplianceAudit, POSHCommitteeMember, POSHCase, PolicyAcknowledgment

@login_required
def compliance_dashboard(request):
    registers = StatutoryRegister.objects.all()[:6]
    audits = ComplianceAudit.objects.all()[:5]
    posh_members = POSHCommitteeMember.objects.filter(is_active=True).select_related('employee')
    total_acks = PolicyAcknowledgment.objects.count()
    
    context = {
        'registers': registers,
        'audits': audits,
        'posh_members': posh_members,
        'total_acks': total_acks,
    }
    return render(request, 'compliance/dashboard.html', context)

@login_required
def register_list(request):
    registers = StatutoryRegister.objects.all()
    return render(request, 'compliance/register_list.html', {'registers': registers})

@login_required
def audit_list(request):
    audits = ComplianceAudit.objects.all()
    return render(request, 'compliance/audit_list.html', {'audits': audits})

@login_required
def posh_portal(request):
    posh_members = POSHCommitteeMember.objects.filter(is_active=True).select_related('employee')
    return render(request, 'compliance/posh_portal.html', {'posh_members': posh_members})
