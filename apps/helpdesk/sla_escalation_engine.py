import datetime
from typing import Dict, Any
from django.utils import timezone
from apps.helpdesk.models import SupportTicket

class HelpdeskSLAEngine:
    '''
    Evaluates Support Ticket SLA deadlines (Priority P1: 4h, P2: 12h, P3: 24h, P4: 48h),
    triggers automated escalations, and computes team resolution efficiency.
    '''

    SLA_HOURS_BY_PRIORITY = {
        'URGENT': 4,
        'HIGH': 12,
        'MEDIUM': 24,
        'LOW': 48,
    }

    @classmethod
    def audit_sla_breaches(cls) -> Dict[str, Any]:
        open_tickets = SupportTicket.objects.filter(status__in=['OPEN', 'IN_PROGRESS', 'PENDING'])
        breached_count = 0
        at_risk_count = 0
        now = timezone.now()

        for t in open_tickets:
            allowed_hrs = cls.SLA_HOURS_BY_PRIORITY.get(getattr(t, 'priority', 'MEDIUM'), 24)
            deadline = t.created_at + datetime.timedelta(hours=allowed_hrs)
            if now > deadline:
                breached_count += 1
            elif (deadline - now).total_seconds() < 7200:  # within 2 hours
                at_risk_count += 1

        total_open = open_tickets.count()
        sla_compliance_pct = round(((total_open - breached_count) / total_open * 100.0), 1) if total_open > 0 else 100.0

        return {
            'total_open_tickets': total_open,
            'breached_sla_count': breached_count,
            'at_risk_count': at_risk_count,
            'sla_compliance_rate': sla_compliance_pct,
        }
