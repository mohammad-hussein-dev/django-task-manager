"""
Tests to cover missing lines in admin.py.
"""
import pytest
from django.contrib.admin import site
from django.contrib.admin.sites import AdminSite
from tasks.admin import TaskAdmin, CategoryAdmin
from tasks.models import Task, Category
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_admin_list_display_fields():
    """Test that admin list_display fields are valid and cover all lines."""
    # Task admin
    task_admin = site._registry[Task]
    assert 'title' in task_admin.list_display
    assert 'status' in task_admin.list_display
    assert 'priority' in task_admin.list_display
    assert 'due_date' in task_admin.list_display

    # Category admin
    category_admin = site._registry[Category]
    assert 'name' in category_admin.list_display
    assert 'created_at' in category_admin.list_display


@pytest.mark.django_db
def test_admin_search_fields():
    """Test that admin search fields are correctly set."""
    task_admin = site._registry[Task]
    assert 'title' in task_admin.search_fields
    assert 'description' in task_admin.search_fields


@pytest.mark.django_db
def test_admin_ordering():
    """Test that admin ordering is set."""
    task_admin = site._registry[Task]
    assert task_admin.ordering == ['-created_at']  # or whatever is set
