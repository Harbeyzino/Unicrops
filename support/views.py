from django.shortcuts import render
from django.views.generic import ListView
from .models import Support

class SupportListView(ListView):
    model = Support
    template_name = 'support/support_list.html'
    context_object_name = 'supports'

# Create your views here.
