"""
Models for the tasks application.

This module defines the Task and Category models with relationships
to Django's User model, along with useful methods and meta options.
"""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Category model for organizing tasks.

    Each category belongs to a specific user and can be color-coded
    for visual identification in the UI.
    """

    # The user who owns this category.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name=_("User"),
    )

    # Category name (e.g., "Work", "Personal", "Shopping")
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
    )

    # Timestamp when the category was created.
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
    )

    class Meta:
        # Order by name, and ensure unique names per user.
        ordering = ["name"]
        unique_together = ("user", "name")
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        """Return the URL to the task list filtered by this category."""
        return reverse("tasks:task_list") + f"?category={self.id}"


class Task(models.Model):
    """
    Task model representing a single to-do item.

    Each task belongs to a user, optionally to a category, and has
    status, priority, and due date fields.
    """

    # Priority choices
    PRIORITY_CHOICES = [
        ("low", _("Low")),
        ("medium", _("Medium")),
        ("high", _("High")),
    ]

    # Status choices
    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("in_progress", _("In Progress")),
        ("completed", _("Completed")),
    ]

    # The user who owns this task.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name=_("User"),
    )

    # Task title (required)
    title = models.CharField(
        max_length=200,
        verbose_name=_("Title"),
    )

    # Optional detailed description
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
    )

    # Optional due date
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Due Date"),
    )

    # Priority level
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
        verbose_name=_("Priority"),
    )

    # Current status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )

    # Optional category (foreign key)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
        verbose_name=_("Category"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        ordering = ["due_date", "-priority"]
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        """Return the URL to the task detail view."""
        return reverse("tasks:task_detail", kwargs={"pk": self.pk})
