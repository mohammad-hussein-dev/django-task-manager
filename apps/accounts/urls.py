"""
URL configuration for the accounts application.

This module defines authentication-related URL patterns:
- Login, logout, and registration.
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

# Namespace for the accounts app — used in reverse() and template {% url %}
app_name = "accounts"

urlpatterns = [
    # Login page
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    # Logout (POST only for security)
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="accounts:login"),
        name="logout",
    ),
    # Registration page
    path("register/", views.RegisterView.as_view(), name="register"),
]
