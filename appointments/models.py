# models.py
from django.db import models
from django.utils import timezone
import uuid
from datetime import time
from datetime import datetime, time, timedelta, date

CONTACT_METHODS = (
    ('zoom', 'Zoom'),
    ('phone', 'Phone Call'),
    ('whatsapp', 'WhatsApp Call'),
)

REASONS = (
    ('branding', 'Branding and Consultancy'),
    ('marketing', 'Digital Marketing'),
    ('social_media', 'Social Media Management'),
    ('graphics', 'Graphics Design'),
    ('web_dev', 'Website and App Development'),
    ('auditing', 'Account Auditing'),
    ('customer_service', 'Customer Service Optimization'),
    ('hr_management', 'Human Resources Management'),
    ('financial_advisory', 'Funding and Financial Advisory'),
    ('other', 'Other'),
)

class DayTemplate(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    day = models.IntegerField(choices=DAYS_OF_WEEK, unique=True)
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_day_display()} ({'Available' if self.is_available else 'Unavailable'})"

class Availability(models.Model):
    date = models.DateField(unique=True)
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    override_template = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Set default start_time and end_time if not provided
        if self.is_available:
            if not self.start_time:
                self.start_time = time(9, 0)  # Default to 9:00 AM
            if not self.end_time:
                self.end_time = time(17, 0)  # Default to 5:00 PM

        # Ensure start_time and end_time are valid datetime.time objects
        if self.is_available and (not isinstance(self.start_time, time) or not isinstance(self.end_time, time)):
            raise TypeError("start_time and end_time must be of type datetime.time")

        super().save(*args, **kwargs)

        # Generate time slots if the availability is active
        if self.is_available:
            self.generate_time_slots()

    def generate_time_slots(self, interval_minutes=30):
        """Generate time slots between start_time and end_time"""
        # Clear existing slots
        self.time_slots.all().delete()
        
        # Ensure start_time and end_time are datetime.time objects
        current_time = self.start_time
        end_time = self.end_time
        
        if not isinstance(current_time, time) or not isinstance(end_time, time):
            raise TypeError("start_time and end_time must be of type datetime.time")
        
        # Generate slots
        while current_time < end_time:
            slot_end = (datetime.combine(datetime.min, current_time) + 
                        timedelta(minutes=interval_minutes)).time()
            
            # Don't create slots that would extend beyond availability end time
            if slot_end > end_time:
                break
                
            TimeSlot.objects.create(
                availability=self,
                time=current_time,
                end_time=slot_end
            )
            
            current_time = slot_end

    def __str__(self):
        return f"{self.date} ({'Available' if self.is_available else 'Unavailable'})"

    @staticmethod
    def generate_availability_from_template():
        today = date.today()
        end_date = today + timedelta(days=60)  # Generate for the next 60 days
        day_templates = {template.day: template for template in DayTemplate.objects.all()}

        for single_date in (today + timedelta(days=n) for n in range((end_date - today).days + 1)):
            day_of_week = single_date.weekday()
            template = day_templates.get(day_of_week)

            if template and template.is_available:
                Availability.objects.update_or_create(
                    date=single_date,
                    defaults={
                        'is_available': template.is_available,
                        'start_time': template.start_time,
                        'end_time': template.end_time,
                        'override_template': False,
                    }
                )

class TimeSlot(models.Model):
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, related_name="time_slots")
    time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['time']
        unique_together = ('availability', 'time')
    
    def __str__(self):
        status = "Booked" if self.is_booked else "Available"
        return f"{self.time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')} ({status})"

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    reason = models.CharField(max_length=50, choices=REASONS)
    custom_reason = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.CharField(default='WAT', max_length=10)
    contact_method = models.CharField(max_length=20, choices=CONTACT_METHODS)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name="appointments")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_contact = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['timeslot__availability__date', 'timeslot__time']
    
    def __str__(self):
        return f"{self.name} - {self.timeslot}"
    
    def save(self, *args, **kwargs):
        # Mark timeslot as booked when appointment is created
        if not self.pk:  # Only on creation
            self.timeslot.is_booked = True
            self.timeslot.save()
        super().save(*args, **kwargs)



