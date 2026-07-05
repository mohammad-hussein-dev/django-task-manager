"""
ASGI config for task_manager project.

This module exposes the ASGI (Asynchronous Server Gateway Interface) callable
as a module-level variable named ``application``. It serves as the entry point
for production ASGI servers (e.g., Daphne, Uvicorn, Hypercorn) and is required
for running the project with asynchronous capabilities, such as WebSockets,
long-polling, or Django Channels.

For more information on this file, see:
    https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set the default Django settings module for ASGI-based environments.
# This allows the ASGI server to locate the project's configuration without
# requiring the DJANGO_SETTINGS_MODULE environment variable to be set manually.
# The value must match the actual Python path to the settings module.
#
# This is the same setting as in wsgi.py, but required separately for ASGI
# to ensure the correct settings are loaded when using asynchronous servers.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

# Create the ASGI application instance.
# This callable is used by ASGI servers to handle incoming requests in an
# asynchronous manner. It loads the settings and initializes the Django
# application stack once, making it efficient for production environments.
#
# Unlike WSGI, ASGI supports both synchronous and asynchronous request
# handling, making it ideal for modern applications that require real-time
# features such as notifications, chat, or streaming responses.
application = get_asgi_application()
