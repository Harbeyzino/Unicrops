from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    subject = 'Welcome to Unicrops!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    context = {
        'user': user,
        'confirm_url': request.build_absolute_uri(reverse('confirm_email', args=[user.id]))
    }
    text_content = 'Thank you for signing up with Unicrops. Please confirm your email address to complete your registration.'
    html_content = render_to_string('email/welcome_email.html', context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    # Set session flag for redirection only for Google sign-up
    if user.socialaccount_set.filter(provider='google').exists():
        request.session['confirmation_email_sent'] = True
