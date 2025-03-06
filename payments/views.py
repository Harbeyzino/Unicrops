from django.shortcuts import render
from django.views.generic import ListView
from .models import Payment

class PaymentListView(ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'

# Create your views here.
