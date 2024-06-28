from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import logout
from django.shortcuts import redirect
from allauth.account.models import EmailAddress

@receiver(user_logged_in)
def check_verified_email(sender, request, user, **kwargs):
    if not EmailAddress.objects.filter(user=user, verified=True).exists():
        # Email is not verified; delete user and log them out
        user.delete()
        logout(request)
        # Optionally redirect to a specific page
        return redirect('account_login')
