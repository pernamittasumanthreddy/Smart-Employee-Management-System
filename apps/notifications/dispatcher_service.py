from typing import List, Dict, Any
from django.utils import timezone
from apps.notifications.models import Notification
from apps.employees.models import Employee

class MultiChannelNotificationDispatcher:
    '''
    Real-time Notification Dispatcher with in-app alerting, priority tagging,
    and bulk batch dispatching.
    '''

    @staticmethod
    def send_notification(recipient: Employee, title: str, message: str, notification_type: str = 'INFO', action_url: str = '') -> Notification:
        return Notification.objects.create(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
            action_url=action_url,
            is_read=False
        )

    @classmethod
    def broadcast_to_department(cls, department_id: int, title: str, message: str, notification_type: str = 'INFO') -> int:
        employees = Employee.objects.filter(department_id=department_id)
        notifications = [
            Notification(
                recipient=emp,
                title=title,
                message=message,
                notification_type=notification_type,
                is_read=False
            ) for emp in employees
        ]
        created = Notification.objects.bulk_create(notifications)
        return len(created)
