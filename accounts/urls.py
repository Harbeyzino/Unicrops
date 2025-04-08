from django.urls import path
from . import views
from .views import user_dashboard, settings_view

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('confirm/<int:user_id>/', views.confirm_email, name='confirm_email'),
    path('confirmation-email-sent/', views.confirmation_email_sent, name='confirmation_email_sent'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('profile/', views.profile, name='profile'),
    path('settings/', settings_view, name='settings'),
    path('pages-error-404/', views.error_404, name='pages-error-404'),

]