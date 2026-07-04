"""
Admin configuration for the tasks application.

This module registers the Task and Category models with the Django admin
interface, providing a clean and efficient way to manage task data.

The admin interface is configured to enable:
- Quick overview of tasks and categories via list views
- Filtering and searching capabilities for efficient data management
- Bulk actions for status updates
- Read-only timestamps to preserve data integrity
"""

from django.contrib import admin

from .models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.

    Provides a simple, searchable list interface for managing task categories.
    Categories are displayed alphabetically for easy navigation.
    """

    # Columns displayed in the list view — shows key fields at a glance.
    list_display = ("id", "name", "created_at")

    # Fields that can be searched — enables quick category lookup by name.
    search_fields = ("name",)

    # Fields that can be filtered — useful for seeing when categories were created.
    list_filter = ("created_at",)

    # Default ordering — categories are listed alphabetically by name.
    ordering = ("name",)

    # Read-only fields — prevents accidental modification of timestamps.
    readonly_fields = ("created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Task model.

    Provides a comprehensive, feature-rich interface for managing tasks with:
    - Quick status overview using color-coded badges (via template override)
    - Powerful filtering and search across task data
    - Bulk actions for updating status
    - Organized form layout with collapsible sections
    """

    # Columns displayed in the list view — provides a complete overview
    # of each task's key attributes for efficient scanning.
    list_display = (
        "id",
        "title",
        "status",
        "priority",
        "category",
        "user",
        "due_date",
        "created_at",
    )

    # Fields that can be searched — enables text-based search across
    # task titles, descriptions, and associated usernames.
    search_fields = ("title", "description", "user__username")

    # Fields that can be filtered — allows users to narrow down the list
    # by status, priority, category, user, or due date.
    list_filter = ("status", "priority", "category", "user", "due_date")

    # Default ordering — newest tasks appear first for better visibility.
    ordering = ("-created_at",)

    # Read-only fields — timestamps are set automatically by Django and
    # should not be modified manually to maintain data integrity.
    readonly_fields = ("created_at", "updated_at")

    # Fieldsets organize the edit form into logical groups, improving
    # the user experience when managing individual tasks.
    fieldsets = (
        # Primary task information — core fields that define the task.
        ("Task Information", {"fields": ("title", "description", "user", "category")}),
        # Status and scheduling — fields that determine the task's
        # progress and deadline.
        ("Status & Priority", {"fields": ("status", "priority", "due_date")}),
        # System timestamps — read-only and collapsible to avoid clutter.
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),  # Collapsible section to save space
            },
        ),
    )

    # Bulk actions — enables admins to update multiple tasks at once.
    actions = ["mark_as_completed", "mark_as_pending"]

    def mark_as_completed(self, request, queryset) -> None:
        """Set the status of selected tasks to 'completed' in bulk."""
        queryset.update(status="completed")

    mark_as_completed.short_description = "Mark selected tasks as completed"

    def mark_as_pending(self, request, queryset) -> None:
        """Set the status of selected tasks to 'pending' in bulk."""
        queryset.update(status="pending")

    mark_as_pending.short_description = "Mark selected tasks as pending"
