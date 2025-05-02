from django.urls import path
from .views import dashboard_view, admin_profile_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('admin-profile/', admin_profile_view, name='admin_profile'),  # Updated URL for admin profile
]
