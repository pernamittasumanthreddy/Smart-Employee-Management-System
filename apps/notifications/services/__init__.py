from apps.notifications.models import Notification


class NotificationService:
    @staticmethod
    def create_notification(user, title, message, category='SYSTEM', link=None):
        if not user:
            return None
        return Notification.objects.create(
            recipient=user,
            title=title,
            message=message,
            category=category,
            link=link
        )

    @staticmethod
    def broadcast_notification(users, title, message, category='ANNC', link=None):
        notifications = [
            Notification(
                recipient=user,
                title=title,
                message=message,
                category=category,
                link=link
            )
            for user in users
        ]
        return Notification.objects.bulk_create(notifications)
