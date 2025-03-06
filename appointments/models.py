from django.db import models

class Appointment(models.Model):
    date = models.DateTimeField()
    client_name = models.CharField(max_length=200)
    service = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.client_name} - {self.service} on {self.date}"

# Create your models here.
