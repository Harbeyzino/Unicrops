# appointments/management/commands/generate_time_slots.py
from django.core.management.base import BaseCommand
from appointments.models import Availability
from datetime import date, time, timedelta

class Command(BaseCommand):
    help = 'Generate time slots for availability'

    def handle(self, *args, **kwargs):
        today = date.today()
        end_date = today + timedelta(days=60)  # Generate for the next 60 days

        for single_date in (today + timedelta(days=n) for n in range((end_date - today).days + 1)):
            Availability.objects.get_or_create(
                date=single_date,
                defaults={
                    'is_available': True,
                    'start_time': time(9, 0),  # Default to 9:00 AM
                    'end_time': time(17, 0),  # Default to 5:00 PM
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully generated time slots for availability'))