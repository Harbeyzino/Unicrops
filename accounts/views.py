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
from django.conf.urls import handler404
import sweetify
from .decorator import unauthenticated_user, admin_only, allowed_users

"""
This module contains views for user authentication, including login, signup, email confirmation,
profile management, and settings. It also includes custom error handling for 404 and 500 errors.

"""

# Security 

# User Login
@unauthenticated_user
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
@unauthenticated_user
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
@unauthenticated_user
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


# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

class PrivacyPolicyView(TemplateView):
    template_name = 'accounts/privacy_policy.html'



"""
        Custom Error Handling
        This section includes custom error handlers for 404 and 500 errors.
        These handlers render specific templates for each error.
        
"""


def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)

def custom_500(request):
    """Custom 500 error handler"""
    return render(request, '500.html', status=500)
    


"""
        User Dashboard and Profile View
        This section includes views for the user dashboard and profile page.

"""

# User Dashboard
@login_required
@allowed_users(allowed_roles=['client', 'admin'])
def user_dashboard(request):
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
    return render(request, 'accounts/dashboard.html', {
        'greeting': greeting,
        'icon': icon,
    })

# User Profile
@login_required
@allowed_users(allowed_roles=['client', 'admin'])
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Update profile fields
        profile.full_name = request.POST.get("full_name", profile.full_name)
        profile.about = request.POST.get("about", profile.about)
        profile.company = request.POST.get("company", profile.company)
        profile.role = request.POST.get("role", profile.role)
        profile.country = request.POST.get("country", profile.country)
        profile.address = request.POST.get("address", profile.address)
        profile.phone_number = request.POST.get("phone_number", profile.phone_number)

        # Update profile picture if uploaded
        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]

        # Update user email
        user.email = request.POST.get("email", user.email)
        user.save()

        # Save the profile
        try:
            profile.save()
            messages.success(request, "Profile updated successfully!")
        except Exception as e:
            messages.error(request, f"Error saving profile: {e}")

    return render(request, "accounts/profile.html", {"profile": profile})


# Edit Profile
@login_required
@allowed_users(allowed_roles=['client', 'admin'])
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        profile = user.profile

        # Update profile fields
        profile.full_name = request.POST.get("full_name")
        profile.about = request.POST.get("about")
        profile.company = request.POST.get("company")
        profile.role = request.POST.get("role")
        profile.country = request.POST.get("country")
        profile.address = request.POST.get("address")
        profile.phone_number = request.POST.get("phone_number")

        # Handle profile picture update
        if "profile_picture" in request.FILES:
            profile.profile_picture = request.FILES["profile_picture"]

        try:
            profile.save()
            user.email = request.POST.get("email")
            user.save()

            # Add Sweetify success message
            sweetify.success(
                request,
                "Profile Updated!",
                text="Your profile was successfully updated.",
                persistent="Ok",
                timer=1000
            )
        except Exception as e:
            # Add Sweetify error message
            sweetify.error(
                request,
                "Update Failed",
                text=f"An error occurred: {e}",
                persistent="Retry",
                timer=1000
            )

        return redirect("profile")

    return render(request, "accounts/profile.html", {"user": request.user})


@login_required
@admin_only
def settings_view(request):
    """Render the settings page."""
    return render(request, 'accounts/settings.html')

def no_permission_view(request):
    """Render the no permission page."""
    return render(request, 'accounts/no_permission.html')
