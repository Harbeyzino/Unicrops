# appointments/apps.py
from django.apps import AppConfig

class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'
    
    def ready(self):
        # Remove all APScheduler code from here
        pass