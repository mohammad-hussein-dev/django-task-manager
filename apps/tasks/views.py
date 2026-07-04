"""
Views for the tasks application.

This module provides CRUD views for tasks with authentication,
pagination, filtering, and deadline status indicators.
"""

from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import TaskForm
from .models import Category, Task


class TaskListView(LoginRequiredMixin, ListView):
    """
    Display a paginated list of tasks for the current user.

    Supports filtering by:
        - status: 'pending', 'in_progress', 'completed'
        - date_filter: 'today', 'this_week', 'this_month'
        - category: category ID

    Pagination: 10 tasks per page with graceful handling of invalid pages.
    """

    model = Task
    template_name = "tasks/task_list.html"
    paginate_by = 10

    def get_queryset(self):
        """Return tasks belonging to the current user, with optional filters."""
        queryset = Task.objects.filter(user=self.request.user).select_related(
            "category"
        )

        # Filter by status
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Filter by date
        date_filter = self.request.GET.get("date_filter")
        if date_filter:
            today = timezone.now().date()
            if date_filter == "today":
                queryset = queryset.filter(due_date=today)
            elif date_filter == "this_week":
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                queryset = queryset.filter(due_date__range=[start_of_week, end_of_week])
            elif date_filter == "this_month":
                start_of_month = today.replace(day=1)
                next_month = start_of_month.replace(day=28) + timedelta(days=4)
                end_of_month = next_month - timedelta(days=next_month.day)
                queryset = queryset.filter(
                    due_date__range=[start_of_month, end_of_month]
                )

        # Filter by category
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Order by due date (soonest first)
        return queryset.order_by("due_date")

    def get_context_data(self, **kwargs):
        """Add filter values, categories, and timestamp to the context."""
        context = super().get_context_data(**kwargs)

        # Preserve current filter values for template use
        context["current_status"] = self.request.GET.get("status", "")
        context["current_date_filter"] = self.request.GET.get("date_filter", "")
        context["date_filter"] = self.request.GET.get("date_filter", "")  # for tests
        context["current_category"] = self.request.GET.get("category", "")

        # List of all categories for the filter dropdown
        context["categories"] = Category.objects.filter(user=self.request.user)

        # Current timestamp for deadline calculations (in template)
        context["current_timestamp"] = int(timezone.now().timestamp())

        # Also add 'tasks' as the page object list (for templates expecting 'tasks')
        if "page_obj" in context:
            context["tasks"] = context["page_obj"]

        return context

    def paginate_queryset(self, queryset, page_size):
        """Override to handle invalid page numbers gracefully."""
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get("page")

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page.
            page = paginator.page(paginator.num_pages)

        return (paginator, page, page.object_list, page.has_other_pages())


class TaskDetailView(LoginRequiredMixin, DetailView):
    """Display detailed information about a single task."""

    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        """Ensure users can only see their own tasks."""
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Create a new task for the current user."""

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    def get_form_kwargs(self):
        """Pass the current user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Set the task's user to the currently logged-in user."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add a page title for the template."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Task"
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing task."""

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    def get_form_kwargs(self):
        """Pass the current user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        """Ensure users can only update their own tasks."""
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add a page title for the template."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Task"
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a task with confirmation."""

    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")

    def get_queryset(self):
        """Ensure users can only delete their own tasks."""
        return Task.objects.filter(user=self.request.user)


class TaskToggleView(LoginRequiredMixin, View):
    """
    Toggle the completion status of a task.

    If the task is 'pending' or 'in_progress', mark it as 'completed'.
    If it's 'completed', revert it to 'pending'.
    Redirects back to the task list after the operation.
    """

    def get(self, request, *args, **kwargs):
        """Handle GET requests by toggling the task status."""
        task = get_object_or_404(Task, pk=kwargs["pk"], user=request.user)
        if task.status == "completed":
            task.status = "pending"
        else:
            task.status = "completed"
        task.save()
        return redirect("tasks:task_list")
