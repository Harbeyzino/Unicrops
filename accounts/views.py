from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.views.generic import TemplateView

"""
User Authentication system
"""

def login_page(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')


# Sign-up view: handles user registration without using a form and stores data
def signup_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Send confirmation email
        subject = 'Welcome to Unicrops'
        confirmation_link = request.build_absolute_uri(reverse('confirm_email', args=[user.id]))
        message = f'Hi {username}, thank you for registering at Unicrops. Please confirm your email address by clicking the link below:\n\n{confirmation_link}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        
        return redirect('confirmation_email_sent')
    return render (request, "accounts/signup.html")

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
    return redirect('login')

class PrivacyPolicyView(TemplateView):
    template_name = 'accounts/privacy_policy.html'





