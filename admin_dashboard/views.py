from django.shortcuts import render, redirect
from accounts.decorator import admin_only
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AdminProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AdminProfileForm
from django.conf import settings
from admin_dashboard.task_management.models import Task  # Import Task model
from notifications.models import Notification  # Import Notification model
from django.utils import timezone  # Import timezone
from django.core.exceptions import FieldError  # Import FieldError
import os

@login_required
# @admin_only
def dashboard_view(request):
    if not request.user.is_staff:
        return redirect('home')
    
    # Task statistics
    all_tasks = Task.objects.all()
    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(is_completed=True).count()
    completion_percentage = round((completed_tasks/total_tasks)*100) if total_tasks > 0 else 0
    
    # Overdue and urgent tasks
    overdue_tasks = Task.objects.filter(
        end_date__lt=timezone.now(),
        is_completed=False
    )
    urgent_tasks = overdue_tasks.filter(priority='high').count() if hasattr(Task, 'priority') else 0
    
    # Recent activity
    try:
        recent_notifications = Notification.objects.filter(
            user=request.user,
            read=False
        ).order_by('-created_at')[:5]
        unread_notifications = Notification.objects.filter(
            user=request.user,
            read=False
        ).count()
    except FieldError:
        recent_notifications = Notification.objects.filter(
            read=False
        ).order_by('-created_at')[:5]
        unread_notifications = Notification.objects.filter(
            read=False
        ).count()
    
    # Recent tasks for table
    recent_tasks = Task.objects.all().order_by('-created_at')[:10]
    
    context = {
        # For the cards
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_percentage': completion_percentage,
        'overdue_tasks_count': overdue_tasks.count(),
        'urgent_tasks': urgent_tasks,
        'recent_notifications': recent_notifications,
        'unread_notifications': unread_notifications,
        
        # For the table
        'recent_tasks': recent_tasks,
        'timezone_now': timezone.now(),
        
        # Original variables for backward compatibility
        'overdue_tasks': overdue_tasks,
    }
    
    return render(request, 'admin_portal/dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_profile(request):
    profile, created = AdminProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('admin_profile')
    else:
        form = AdminProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'profile_picture_url': profile.get_profile_picture()
    }
    return render(request, 'admin_portal/profile.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_profile_picture(request):
    profile = request.user.admin_profile
    if profile.profile_picture and profile.profile_picture.name != 'admin_default.png':
        try:
            if os.path.exists(profile.profile_picture.path):
                os.remove(profile.profile_picture.path)
        except Exception as e:
            messages.error(request, f"Error removing picture: {str(e)}")
        profile.profile_picture = 'admin_default.png'
        profile.save()
        messages.success(request, 'Profile picture removed!')
    return redirect('admin_profile')


@login_required
def all_notifications(request):
    # Mark all notifications as read when viewing this page
    Notification.objects.filter(user=request.user, read=False).update(read=True)
    
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'admin_portal/all_notifications.html', {
        'notifications': notifications
    })