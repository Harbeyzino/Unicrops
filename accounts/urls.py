from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('confirm/<int:user_id>/', views.confirm_email, name='confirm_email'),
    path('confirmation-email-sent/', views.confirmation_email_sent, name='confirmation_email_sent'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]
