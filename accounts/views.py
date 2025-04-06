from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.utils.timezone import now
from datetime import datetime


# User Login
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

# User Signup
def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Try another one.")
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
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        messages.success(request, "Registration successful! Check your email to confirm your account.")
        return redirect('confirmation_email_sent')

    return render(request, "accounts/signup.html")

# Email Confirmation
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


@login_required
def user_dashboard(request):
    """Fetch or create user profile data for the dashboard"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/dashboard.html', {'profile': profile})

@login_required
def profile(request):
    """Fetch and pass profile data to the profile page"""
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

class PrivacyPolicyView(TemplateView):
    template_name = 'accounts/privacy_policy.html'

@login_required
def settings_view(request):
    """Render the settings page."""
    return render(request, 'accounts/settings.html')


def adminHome(request):
    # Determine the greeting based on the time of day
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning"
        icon = "🌞"  # Sun icon
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon"
        icon = "☀️"  # Bright sun icon
    else:
        greeting = "Good Evening"
        icon = "🌙"  # Moon icon

    # Pass greeting and icon to the template
    return render(request, 'digiApp/admin-portal/adhome.html', {
        'greeting': greeting,
        'icon': icon,
    })
