"""
URL configuration for the tasks application.

This module defines all URL patterns for task management, including:
- Listing tasks with filters and pagination
- Creating, updating, and deleting tasks
- Viewing task details
- Toggling task completion status
"""

from django.urls import path

from . import views

# Namespace for the tasks app — used in reverse() and template {% url %}
app_name = "tasks"

urlpatterns = [
    # Task list with filters and pagination
    path("", views.TaskListView.as_view(), name="task_list"),
    # Task detail view
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    # Create a new task
    path("create/", views.TaskCreateView.as_view(), name="task_create"),
    # Update an existing task
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="task_update"),
    # Delete a task with confirmation
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    # Toggle task completion status (used in task list)
    path("<int:pk>/toggle/", views.TaskToggleView.as_view(), name="task_toggle"),
]
