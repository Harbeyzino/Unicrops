# management/commands/generate_availability.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from appointments.models import DayTemplate, Availability

class Command(BaseCommand):
    help = 'Generates availability for the next 60 days based on day templates'
    
    def handle(self, *args, **options):
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=60)
        
        for day_template in DayTemplate.objects.filter(is_available=True):
            current_date = start_date
            while current_date <= end_date:
                if current_date.weekday() == day_template.day:
                    Availability.objects.get_or_create(
                        date=current_date,
                        defaults={
                            'start_time': day_template.start_time,
                            'end_time': day_template.end_time,
                            'is_available': True
                        }
                    )
                current_date += timedelta(days=1)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully generated availability until {end_date}'))