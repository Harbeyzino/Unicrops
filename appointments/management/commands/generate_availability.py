from django.core.management.base import BaseCommand
from appointments.models import Availability

class Command(BaseCommand):
    help = 'Generate availability for the next 60 days based on day templates'

    def handle(self, *args, **kwargs):
        Availability.generate_availability_from_template()
        self.stdout.write(self.style.SUCCESS('Successfully generated availability for the next 60 days.'))
