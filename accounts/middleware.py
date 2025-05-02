from django.shortcuts import redirect
from django.conf import settings

class RoleBasedAccessMiddleware:
    """
    Middleware to handle access control based on user roles (admin or regular user)
    and enforce authentication for accessing specific views.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is authenticated
        if request.user.is_authenticated:
            # Handle redirection based on user roles

            # Allow admins to access the product page
            if request.path.startswith('/product/') and request.user.is_staff:
                return self.get_response(request)

            # Regular user trying to access the product page -> redirect to the appropriate page
            elif request.path.startswith('/product/') and not request.user.is_staff:
                return redirect('app.no_permission')  # Change this if needed

            # Regular user trying to access the admin portal -> redirect to the no permission page
            elif request.path.startswith('/ad_dashboard/') and not request.user.is_staff:
                return redirect('app.no_permission')  # Redirect to the no_permission page

        else:
            # If the user is not authenticated and trying to access protected pages
            protected_paths = [
                '/ad_dashboard/',  # Admin dashboard
                '/product/',       # Product page
                '/accounts/'       # Accounts page (if needed)
                
            ]
            if any(request.path.startswith(path) for path in protected_paths):
                return redirect(settings.LOGIN_URL)  # Redirect to login page if not authenticated

        # Continue processing the request if none of the conditions apply
        response = self.get_response(request)
        return response