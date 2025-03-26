from django.shortcuts import render
from accounts.models import Profile  # Ensure the correct import


def home_page(request):
    """Display the home page with user profile if logged in"""
    profile = None  # Default to None if the user is not logged in
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)  # Ensure profile exists

    return render(request, 'home.html', {'profile': profile})


