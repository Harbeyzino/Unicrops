from django.shortcuts import render
from calendar import HTMLCalendar, month_name
from datetime import date, datetime
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Availability, TimeSlot, DayTemplate
from django.views.decorators.http import require_GET
from .models import TimeSlot, Availability



class CustomHTMLCalendar(HTMLCalendar):
    def __init__(self, available_dates=None):
        super().__init__()
        self.available_dates = available_dates or []

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        date_str = f"{self.year}-{self.month:02d}-{day:02d}"
        is_available = date_str in self.available_dates

        css_class = "calendar-day available" if is_available else "calendar-day unavailable"
        return f'<td class="{css_class}" data-date="{date_str}"><div>{day}</div></td>'

    def formatmonthname(self, theyear, themonth, withyear=True):
        # Override to return an empty string, ignoring the month display
        return ''

    def formatmonth(self, theyear, themonth, withyear=True):
        self.year, self.month = theyear, themonth
        return super().formatmonth(theyear, themonth, withyear)


def book_appointment(request):
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    # Fetch available dates from the database
    available_dates = Availability.objects.filter(
        is_available=True,
        date__year=year,
        date__month=month
    ).values_list('date', flat=True)
    available_dates = [d.strftime('%Y-%m-%d') for d in available_dates]

    # Generate the calendar
    calendar = CustomHTMLCalendar(available_dates).formatmonth(year, month)

    context = {
        'calendar': calendar,
        'current_month': today.strftime('%B'),
        'current_year': today.year,
    }
    return render(request, 'appointments/book_now.html', context)


def get_calendar(request):
    try:
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid month or year'}, status=400)

    requested_date = date(year, month, 1)
    today = date.today()
    min_date = date(today.year, today.month, 1) - relativedelta(months=0)
    max_date = date(today.year, today.month, 1) + relativedelta(months=1)

    # Clamp requested_date within bounds
    if requested_date < min_date:
        requested_date = min_date
    elif requested_date > max_date:
        requested_date = max_date

    calendar_html = CustomHTMLCalendar(year=requested_date.year, month=requested_date.month).formatmonth(
        requested_date.year, 
        requested_date.month
    )

    # Calculate next and previous dates
    next_date = requested_date + relativedelta(months=1)
    prev_date = requested_date - relativedelta(months=1)

    # Determine if buttons should be disabled
    is_next_disabled = next_date > max_date
    is_prev_disabled = prev_date < min_date

    return JsonResponse({
        'calendar': calendar_html,
        'current_month': month_name[requested_date.month],
        'current_year': requested_date.year,
        'prev_month': prev_date.month,
        'prev_year': prev_date.year,
        'next_month': next_date.month,
        'next_year': next_date.year,
        'is_prev_disabled': is_prev_disabled,
        'is_next_disabled': is_next_disabled,
    })


def get_available_dates(request):
    today = date.today()
    end_date = today + timedelta(days=60)
    available_dates = []

    # Fetch day templates
    day_templates = {template.day: template for template in DayTemplate.objects.all()}

    # Generate available dates
    for single_date in (today + timedelta(days=n) for n in range((end_date - today).days + 1)):
        day_of_week = single_date.weekday()
        template = day_templates.get(day_of_week)
        if template and template.is_available:
            available_dates.append(single_date.strftime('%Y-%m-%d'))

    return JsonResponse({'dates': available_dates})

def get_available_times(request):
    date_str = request.GET.get('date')
    
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        availability = Availability.objects.get(date=selected_date, is_available=True)
        
        times = TimeSlot.objects.filter(
            availability=availability,
            is_booked=False
        ).values_list('time', flat=True)
        
        return JsonResponse({
            'times': [time.strftime('%H:%M') for time in times],
            'display_date': selected_date.strftime('%A, %B %d')
        })
        
    except (ValueError, Availability.DoesNotExist):
        return JsonResponse({'error': 'Invalid date or no availability'}, status=400)

def generate_slots(request, availability_id):
    if request.method == 'POST':
        try:
            availability = Availability.objects.get(id=availability_id)
            availability.generate_time_slots()  # Assuming this method exists in your model
            return JsonResponse({'status': 'success', 'message': 'Time slots generated successfully'})
        except Availability.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Availability not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)



@require_GET
def available_time_slots(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date parameter required'}, status=400)
    
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    # First check if the date is available
    try:
        availability = Availability.objects.get(date=selected_date)
        if not availability.is_available:
            return JsonResponse([], safe=False)
    except Availability.DoesNotExist:
        return JsonResponse([], safe=False)
    
    # Get available slots that aren't booked
    slots = TimeSlot.objects.filter(
        availability__date=selected_date,
        availability__is_available=True
    ).select_related('availability').order_by('time')
    
    slot_data = []
    for slot in slots:
        slot_data.append({
            'id': slot.id,
            'start_time': slot.time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M'),
            'is_booked': slot.appointments.exists()
        })
    
    return JsonResponse(slot_data, safe=False)