"""
Views for the accounts application.

This module contains views for user registration.
Login and logout are handled by Django's built-in auth views.
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegisterView(CreateView):
    """
    View for user registration.

    Displays a registration form and creates a new user account upon valid submission.
    On success, redirects to the login page.
    """

    model = User
    form_class = UserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")
