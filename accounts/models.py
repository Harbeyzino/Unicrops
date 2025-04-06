from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

def user_avatar_upload_path(instance, filename):
    # Define the upload path for user avatars
    return f'avatars/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = CloudinaryField('image', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
