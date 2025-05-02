from django.db import models
from django.contrib.auth.models import User

class AdminProfile(models.Model):
    """
    Model for admin profiles, including role name and profile picture.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    role_name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='admin_profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role_name if self.role_name else 'No Role'}"

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

    def __str__(self):
        return f"{self.date} ({'Available' if self.is_available else 'Unavailable'})"

class TimeSlot(models.Model):
    availability = models.ForeignKey(Availability, related_name='time_slots', on_delete=models.CASCADE)
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)  # Fixed syntax error

    def __str__(self):
        return f"{self.availability.date} - {self.time} ({'Booked' if self.is_booked else 'Available'})"

class Appointment(models.Model):
    timeslot = models.ForeignKey(TimeSlot, related_name='appointments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    reason = models.TextField()
    contact_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.name} on {self.timeslot.availability.date} at {self.timeslot.time}"


