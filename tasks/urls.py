"""
URL configuration for the tasks application.

This module defines all URL patterns for task management views,
including listing, detail, create, update, delete, and toggle status.
"""

from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    # Task list with optional filters (status, priority, category, search)
    path("", views.TaskListView.as_view(), name="task_list"),
    # Task detail view
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    # Create a new task
    path("create/", views.TaskCreateView.as_view(), name="task_create"),
    # Update an existing task
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="task_update"),
    # Delete a task with confirmation
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    # Toggle completion status (for quick updates)
    path("<int:pk>/toggle/", views.TaskToggleView.as_view(), name="task_toggle"),
]
