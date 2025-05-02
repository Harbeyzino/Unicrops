from django.urls import path
from . import views

urlpatterns = [
    path('book-now/', views.book_appointment, name='book_appointment'),
    path('get-calendar/', views.get_calendar, name='get_calendar'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),
    path('availability/generate-slots/<int:availability_id>/', views.generate_slots, name='appointments_availability_generate_slots'),
    path('get-available-dates/', views.get_available_dates, name='get_available_dates'),
    path('api/available-time-slots/', views.available_time_slots, name='available_time_slots'),
]