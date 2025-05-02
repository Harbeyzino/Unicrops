# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import DayTemplate, Availability, TimeSlot, Appointment

@admin.register(DayTemplate)
class DayTemplateAdmin(admin.ModelAdmin):
    list_display = ('get_day_display', 'is_available', 'start_time', 'end_time')
    list_editable = ('is_available', 'start_time', 'end_time')
    ordering = ('day',)

    def get_day_display(self, obj):
        return obj.get_day_display()
    get_day_display.short_description = 'Day'

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('date', 'is_available', 'start_time', 'end_time', 'override_template')
    list_filter = ('is_available', 'override_template')
    date_hierarchy = 'date'
    actions = ['generate_availability']

    def generate_availability(self, request, queryset):
        Availability.generate_availability_from_template()
        self.message_user(request, "Availability generated from templates.")
    generate_availability.short_description = "Generate availability from templates"

    def formatted_time_range(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"
    formatted_time_range.short_description = 'Time Range'
    
    def timeslot_count(self, obj):
        return obj.time_slots.count()
    timeslot_count.short_description = 'Slots'
    
    def generate_time_slots(self, request, queryset):
        for availability in queryset:
            availability.generate_time_slots()
        self.message_user(request, f"Generated time slots for {queryset.count()} availabilities")
    generate_time_slots.short_description = "Generate time slots for selected"
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_slots_url'] = '/appointments/availability/generate-slots/'
        self.change_list_template = 'admin/unicrops/availability/change_list.html'
        print("Custom change_list.html is being used.")
        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        print("Custom change_form.html is being used.")
        return super().changeform_view(request, object_id, form_url, extra_context)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    change_list_template = 'admin/unicrops/availability/change_list.html'
    list_display = ('availability', 'formatted_time_range', 'is_booked', 'has_appointment')
    list_filter = ('is_booked', 'availability__date')
    search_fields = ('availability__date',)
    
    def formatted_time_range(self, obj):
        return f"{obj.time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"
    formatted_time_range.short_description = 'Time Slot'
    
    def has_appointment(self, obj):
        return obj.appointments.exists()
    has_appointment.boolean = True
    has_appointment.short_description = 'Booked'
    
    list_filter = (
        ('availability__date', admin.DateFieldListFilter),
        ('is_booked', admin.BooleanFieldListFilter),
        ('time', admin.DateFieldListFilter),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.GET.get('is_booked__exact') == '0':
            return qs.filter(is_booked=False)
        return qs

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        self.change_list_template = 'admin/unicrops/availability/change_list.html'
        return super().changelist_view(request, extra_context)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    change_list_template = 'admin/unicrops/availability/change_list.html'
    list_display = ('name', 'email', 'get_date', 'get_time', 'contact_method', 'reason')
    list_filter = ('contact_method', 'reason', 'timeslot__availability__date')
    search_fields = ('name', 'email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_date(self, obj):
        return obj.timeslot.availability.date
    get_date.short_description = 'Date'
    get_date.admin_order_field = 'timeslot__availability__date'
    
    def get_time(self, obj):
        return f"{obj.timeslot.time.strftime('%H:%M')}-{obj.timeslot.end_time.strftime('%H:%M')}"
    get_time.short_description = 'Time Slot'
    get_time.admin_order_field = 'timeslot__time'