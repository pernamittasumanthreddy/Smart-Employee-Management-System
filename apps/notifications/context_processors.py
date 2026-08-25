from apps.notifications.models import Notification


def notification_context(request):
    if not request.user.is_authenticated:
        return {
            'unread_notifications_count': 0,
            'recent_notifications': [],
        }

    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    recent = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:5]

    return {
        'unread_notifications_count': unread_count,
        'recent_notifications': recent,
    }
