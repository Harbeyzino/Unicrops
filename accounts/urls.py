from django.urls import path
from . import views
from .views import user_dashboard, settings_view

urlpatterns = [
    # User Authentication URLs
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Password Reset URLs / confirmation URLs
    path('confirm/<int:user_id>/', views.confirm_email, name='confirm_email'),
    path('confirmation-email-sent/', views.confirmation_email_sent, name='confirmation_email_sent'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),

    # User Dashboard and Profile URLs
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('settings/', settings_view, name='settings'),

]