from django.shortcuts import render
from django.views.generic import ListView
from .models import Notification

class NotificationListView(ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'

# Create your views here.
