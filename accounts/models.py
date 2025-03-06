from django.db import models
from django.contrib.auth.models import User

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Dashboard"
