from django.urls import path, include
from .views import admin_profile, delete_profile_picture, dashboard_view
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard_view, all_notifications


urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('ad_dashboard/', dashboard_view, name='ad_dashboard'),
    path('profile/', admin_profile, name='admin_profile'),
    path('profile/delete-picture/', delete_profile_picture, name='delete_admin_picture'),
    path('tasks/', include('admin_dashboard.task_management.urls')),
    path('notifications/', all_notifications, name='all_notifications'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)