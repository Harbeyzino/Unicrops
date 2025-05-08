from .models import Notification

def create_notification(user, notification_type, title, message, related_id=None):
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        related_id=related_id
    )