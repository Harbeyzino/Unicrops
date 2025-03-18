from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.shortcuts import resolve_url, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from allauth.core.exceptions import ImmediateHttpResponse

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return resolve_url("user_dashboard")


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """Restrict first-time users and allow them to sign up using the same Google login."""
        email = sociallogin.account.extra_data.get("email")

        if not email:
            return  # No email means we can't process this login.

        user = User.objects.filter(email=email).first()

        if not user:
            # First-time user: store social login in session and redirect to sign-up
            request.session["social_signup_email"] = email
            request.session["social_signup_provider"] = sociallogin.account.provider
            messages.error(request, "No Unicrops account linked to this email. Please sign up first.")
            raise ImmediateHttpResponse(redirect("account_signup"))  # Fixed: Proper redirect handling

        # Existing user: Verify email and proceed
        email_address, created = EmailAddress.objects.get_or_create(user=user, email=email)
        if not email_address.verified:
            email_address.verified = True
            email_address.save()

    def save_user(self, request, sociallogin, form=None):
        """Ensure the user is properly saved and verified"""
        user = super().save_user(request, sociallogin, form)
        email = user.email
        email_address, created = EmailAddress.objects.get_or_create(user=user, email=email)
        if not email_address.verified:
            email_address.verified = True
            email_address.save()

        return user
