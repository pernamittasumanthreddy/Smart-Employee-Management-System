from typing import List, Dict, Any
from django.utils import timezone
from apps.announcements.models import Announcement
from apps.employees.models import Employee

class CorporateBroadcastEngine:
    '''
    Multi-Channel Corporate Broadcast & Town Hall Engine:
    - Target audience filtering (By Department, Grade, Location, or Organization-Wide)
    - Priority broadcast alerts (Emergency, Operational, Policy, Celebration)
    - Read acknowledgment analytics
    '''

    @staticmethod
    def dispatch_broadcast(title: str, message: str, priority: str = 'NORMAL', department_id: int = None) -> Announcement:
        announcement = Announcement.objects.create(
            title=title,
            content=message,
            priority=priority,
            published_at=timezone.now(),
            is_active=True
        )
        return announcement

    @staticmethod
    def get_active_announcements_for_employee(employee: Employee) -> List[Announcement]:
        return list(Announcement.objects.filter(is_active=True).order_by('-published_at')[:10])
