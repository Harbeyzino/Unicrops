from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, SubTask

@receiver(post_save, sender=Task)
def task_created_notification(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        Notification.objects.create(
            user=instance.assigned_to,
            message=f"New task assigned: {instance.title}",
            link=f"/tasks/{instance.id}/"
        )

@receiver(post_save, sender=SubTask)
def subtask_completed_notification(sender, instance, **kwargs):
    if instance.is_completed:
        Notification.objects.create(
            user=instance.task.assigned_to,
            message=f"Subtask completed: {instance.title}",
            link=f"/tasks/{instance.task.id}/"
        )