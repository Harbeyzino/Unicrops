from django.shortcuts import render
from django.views.generic import ListView
from .models import Contact

class ContactListView(ListView):
    model = Contact
    template_name = 'contact/contact_list.html'
    context_object_name = 'contacts'

# Create your views here.
