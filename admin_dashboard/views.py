from django.shortcuts import render, redirect
from accounts.decorator import admin_only
from django.contrib.auth.decorators import login_required
from .models import AdminProfile


# @login_required
# @admin_only
def dashboard_view(request):
    """Render the admin dashboard."""
    return render(request, 'admin_portal/dashboard.html')

# @login_required
# @admin_only
def admin_profile_view(request):
    """Render the admin profile page."""
    admin_profile, created = AdminProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Update role name
        admin_profile.role_name = request.POST.get("role_name", admin_profile.role_name)

        # Update profile picture if provided
        if request.FILES.get("profile_picture"):
            admin_profile.profile_picture = request.FILES["profile_picture"]

        admin_profile.save()
        return redirect('admin_profile')

    return render(request, 'admin_portal/adminProfile.html', {'admin_profile': admin_profile})

