from django.db import models
from django.contrib.auth.models import User
import os

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

    def __str__(self):
        return f"{self.user.username}'s Profile"
