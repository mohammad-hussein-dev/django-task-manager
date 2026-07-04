"""
App configuration for the tasks application.

This module defines the configuration for the tasks app.
"""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Configuration class for the tasks application."""

    # Use BigAutoField as the default primary key type.
    default_auto_field = "django.db.models.BigAutoField"

    # The full Python path to the app — matches INSTALLED_APPS entry.
    name = "apps.tasks"

    # Human-readable name for the admin interface.
    verbose_name = "Tasks / وظایف"

    def ready(self) -> None:
        """Perform any needed initialization when the app is ready."""
        # Import signals here if needed.
        # import tasks.signals  # noqa
        pass
