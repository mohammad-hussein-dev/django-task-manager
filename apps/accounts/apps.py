"""
App configuration for the accounts application.

This module defines the configuration for the accounts app.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration class for the accounts application."""

    # Use BigAutoField as the default primary key type.
    default_auto_field = "django.db.models.BigAutoField"

    # The full Python path to the app — matches INSTALLED_APPS entry.
    name = "apps.accounts"

    # Human-readable name for the admin interface.
    verbose_name = "Accounts / حساب‌ها"

    def ready(self) -> None:
        """Perform any needed initialization when the app is ready."""
        # Import signals here if needed.
        # import accounts.signals  # noqa
        pass
