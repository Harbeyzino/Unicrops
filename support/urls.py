from django.urls import path
from .views import SupportListView

urlpatterns = [
    path('', SupportListView.as_view(), name='support-list'),
]
