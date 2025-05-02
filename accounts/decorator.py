from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

# Decorator to restrict access for already authenticated users
def unauthenticated_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Redirects authenticated users (e.g., staff) from accessing unauthenticated pages
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(reverse('home'))  # Adjust to your home page
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Decorator to allow access only to specified user groups
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            # Check if user belongs to any allowed group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
            # Redirect to no permission page if user lacks the required group
            return redirect('no_permission')  # Replace with your no permission page
        return wrapper_func
    return decorator

# Decorator to restrict view access to admin users only
def admin_only(view_func):
    @wraps(view_func)
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            # Allow access based on role
            if group == 'client':
                return redirect('home')  # Redirect customers to home
            elif group == 'admin':
                return view_func(request, *args, **kwargs)  # Allow admins access

        # Default redirect if user has no group or lacks permissions
        return redirect('no_permission')  # Adjust to a "no permission" page

    return wrapper_function

