from django.db import models

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.method} - {self.amount}"

# Create your models here.
