#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script is the main entry point for all Django management commands,
including running the development server, creating database migrations,
executing tests, and managing the application via the command line.

It sets up the Django environment, loads the project settings, and
delegates the execution to Django's built-in management system.

For more information on this file, see:
    https://docs.djangoproject.com/en/6.0/ref/django-admin/
"""

import os
import sys


def main() -> None:
    """
    Run administrative tasks for the Django project.

    This function is the core of the manage.py script. It:
        1. Sets the DJANGO_SETTINGS_MODULE environment variable to point
           to the project's settings module.
        2. Imports the execute_from_command_line function from Django's
           core management module.
        3. Executes the command-line arguments passed to the script,
           delegating to the appropriate Django management command.

    Raises:
        ImportError: If Django is not installed or not available in the
            current Python environment. This typically occurs when the
            virtual environment is not activated or Django is not installed.
    """
    # Set the default Django settings module for the project.
    # This must match the actual Python path to the settings file.
    # If the environment variable is already set (e.g., by the WSGI server),
    # this line will not override it.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

    try:
        # Import the function that processes command-line arguments
        # and executes the corresponding Django management command.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed or cannot be imported, raise a clear
        # error message to guide the user toward resolving the issue.
        # This is a common error when the virtual environment is not activated
        # or when Django is not installed in the current environment.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Delegate execution to Django's management system.
    # sys.argv contains the command-line arguments passed to the script.
    # The first argument (sys.argv[0]) is the script name, and the rest
    # are the command and its options (e.g., runserver, makemigrations).
    execute_from_command_line(sys.argv)


# This block ensures that the main() function is only executed when the
# script is run directly (not when imported as a module).
# This is a standard Python pattern for scripts that can also be imported.
if __name__ == "__main__":
    main()
