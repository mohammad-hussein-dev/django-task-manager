#!/usr/bin/env python
# =============================================================================
# Django Project Management Script
# =============================================================================
# This script serves as the primary command-line interface (CLI) for managing
# and interacting with the Django project. It provides access to Django's
# built-in administrative commands (e.g., runserver, migrate, shell, etc.).
# =============================================================================

"""
Django's command-line utility for administrative tasks.

This script is the entry point for all Django management commands. It sets up
the necessary environment, configures the Django settings module, and delegates
control to Django's core management system.
"""

import os
import sys
from pathlib import Path

# =============================================================================
# Path Configuration
# =============================================================================
# The project uses a non-standard directory structure where the Django project
# files (manage.py, settings.py, etc.) reside in the 'src/' directory.
# This is a common pattern for better separation of source code and project
# configuration files.
#
# The following code ensures that Python can locate the 'task_manager' module
# and other project packages regardless of the current working directory.
# =============================================================================

# Resolve the absolute path to the directory containing this script (manage.py).
BASE_DIR = Path(__file__).resolve().parent

# Add the 'src/' subdirectory to Python's module search path (sys.path).
# This allows the interpreter to find the Django project modules (task_manager,
# apps, etc.) when running commands from any location.
sys.path.insert(0, str(BASE_DIR / "src"))


def main() -> None:
    """
    Run administrative tasks.

    This function acts as the main entry point for the Django management CLI.
    It performs the following operations:
        1. Sets the default Django settings module to 'task_manager.settings'.
        2. Imports Django's command execution function.
        3. Executes the command passed via command-line arguments.

    If Django is not installed or not found in the Python environment, the
    function raises an informative ImportError to guide the user.
    """
    # Set the environment variable that tells Django which settings module to use.
    # This is required for Django to load the correct configuration.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

    try:
        # Import Django's command execution function.
        # This function parses the command-line arguments and runs the
        # corresponding management command (e.g., runserver, migrate, shell, etc.).
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed or the import fails, raise a detailed error
        # message with troubleshooting tips.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? "
            "Did you forget to activate a virtual environment?"
        ) from exc

    # Delegate control to Django's management system.
    # sys.argv contains the command-line arguments, including the command name
    # and any subcommands or options provided by the user.
    execute_from_command_line(sys.argv)


# =============================================================================
# Script Entry Point
# =============================================================================
# The '__name__ == "__main__"' condition ensures that the main() function is
# called only when this script is executed directly (e.g., via `python manage.py`)
# and not when it is imported as a module in another file.
# =============================================================================
if __name__ == "__main__":
    main()
