from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

def user_avatar_upload_path(instance, filename):
    """Generate a dynamic upload path for user avatars"""
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_avatar_upload_path, null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        """Returns display name if set, otherwise username"""
        return self.displayname if self.displayname else self.user.username

    @property
    def avatar(self):
        """Returns the profile image URL or a default avatar"""
        if self.image and self.image.url:
            return self.image.url
        return os.path.join(settings.STATIC_URL, 'img/avatar.png')
