from django.db import models
from django.contrib.auth.models import User
import os
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def user_avatar_upload_path(instance, filename):
    # Define the upload path for user avatars
    return os.path.join('avatars', instance.user.username, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Use a default profile picture if none is provided
    profile_picture = models.ImageField(
        upload_to=user_avatar_upload_path,
        blank=True,
        null=True,
        default='avatar.png'
    )
    
    address = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('TASK', 'Task Update'),
        ('ORDER', 'Order Update'),
        ('SYSTEM', 'System Notification'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_id = models.PositiveIntegerField(null=True, blank=True)  # For task/order ID
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"