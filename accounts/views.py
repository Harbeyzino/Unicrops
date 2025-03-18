from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.views.generic import TemplateView
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse  # Update this import

"""
User Authentication system
"""

def login_page(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! Welcome back.")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'accounts/login.html')


def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Try another one.")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Try logging in.")

        # If there are errors, redirect back to signup page
        if messages.get_messages(request):
            return redirect('account_signup')

        # Create new user
        user = User.objects.create_user(username=username, password=password, email=email)

        # Send confirmation email
        subject = 'Welcome to Unicrops'
        confirmation_link = request.build_absolute_uri(reverse('confirm_email', args=[user.id]))
        message = f'Hi {username}, thank you for registering at Unicrops. Please confirm your email address by clicking the link below:\n\n{confirmation_link}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, "Registration successful! Check your email to confirm your account.")
        return redirect('confirmation_email_sent')

    return render(request, "accounts/signup.html")


def confirm_email(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        messages.success(request, "Email confirmed successfully! Please log in to continue.")
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, "Invalid confirmation link.")
        return redirect('signup')

def confirmation_email_sent(request):
    return render(request, "accounts/confirmation_email_sent.html")

def dashboard(request):
    return render(request, "accounts/dashboard.html")

def logout_view(request):
    logout(request)
    return redirect('home')

class PrivacyPolicyView(TemplateView):
    template_name = 'accounts/privacy_policy.html'

def profile(request):
    return render(request, 'accounts/profile.html')

def settings(request):
    return render(request, 'accounts/settings.html')

