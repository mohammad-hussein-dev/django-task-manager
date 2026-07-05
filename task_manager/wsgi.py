"""
WSGI config for task_manager project.

This module exposes the WSGI (Web Server Gateway Interface) callable
as a module-level variable named ``application``. It is the entry point
for production WSGI servers (e.g., Gunicorn, uWSGI, Daphne) and is used
by Django's development server as well.

For more information on this file, see:
    https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for WSGI-based environments.
# This allows the WSGI server to locate the project's configuration without
# requiring the DJANGO_SETTINGS_MODULE environment variable to be set manually.
# The value must match the actual Python path to the settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

# Create the WSGI application instance.
# This callable is used by WSGI servers to handle incoming HTTP requests.
# It loads the settings and initializes the Django application stack once,
# making it efficient for production environments.
application = get_wsgi_application()
