from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """Prevent social login if the user does not exist."""
        user = sociallogin.user
        User = get_user_model()
        
        # Check if the user already exists
        if not user.email or not User.objects.filter(email=user.email).exists():
            raise PermissionDenied("You need to sign up first before logging in.")
