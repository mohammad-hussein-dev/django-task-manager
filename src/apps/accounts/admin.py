"""
Admin configuration for the accounts application.

This module customizes the Django admin interface for the User model,
providing a more comprehensive and user-friendly view for managing users
and their associated data.

While no custom models are defined in this app, the default User admin
is enhanced to include additional columns, filters, and search capabilities
that improve the admin experience for staff and superusers.

For more information on Django admin customization, see:
    https://docs.djangoproject.com/en/6.0/ref/contrib/admin/
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.

    Extends Django's default UserAdmin to provide a more informative
    list view, additional filters, and improved search capabilities.

    This customization makes it easier for administrators to manage
    users, view their activity, and quickly locate specific accounts.

    Attributes:
        list_display: Columns displayed in the user list view.
        search_fields: Fields that can be searched in the admin.
        list_filter: Filters available in the sidebar.
        ordering: Default ordering of users in the list.
    """

    # Columns displayed in the user list view.
    # Includes username, email, first/last names, staff status,
    # active status, and last login date for a comprehensive overview.
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
    )

    # Fields that can be searched via the admin search box.
    # Enables quick lookup by username, email, or full name.
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    # Filters available in the sidebar for narrowing down the user list.
    # These filters help administrators quickly find users by status,
    # staff permissions, or account creation date.
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "last_login",
    )

    # Default ordering — users are displayed by date joined (newest first).
    # This ensures that recently registered users appear at the top.
    ordering = ("-date_joined",)


# Unregister the default User admin to replace it with the custom one.
# Django registers the User model by default, so we need to unregister
# it before registering our custom admin configuration.
admin.site.unregister(User)

# Register the User model with the custom admin configuration.
# This applies the enhanced list_display, search_fields, list_filter,
# and ordering defined above to the admin interface.
admin.site.register(User, CustomUserAdmin)
