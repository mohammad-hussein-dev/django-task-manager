"""
App configuration for the tasks application.

This module defines the TasksConfig class for Django's app registry,
allowing customization of the app's behavior and metadata.
"""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """
    Configuration class for the tasks app.

    Attributes:
        default_auto_field: The default primary key field type for models.
        name: The Python path to the app's module (set automatically by Django).
        verbose_name: Human-readable name for the app (displayed in admin).
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"
    verbose_name = "Tasks"

    def ready(self) -> None:
        """
        Perform app initialization tasks.

        This method is called when Django's application registry is fully
        populated. It can be used to import signals or register handlers.
        """
        # Import signals to ensure they are registered
        # import tasks.signals  # Uncomment if signals are added later
        pass
