"""
Tests to cover missing lines in admin.py.
"""
import pytest
from django.contrib.admin import site
from django.test import RequestFactory
from tasks.models import Task, Category


@pytest.mark.django_db
def test_admin_list_display_fields():
    task_admin = site._registry[Task]
    assert 'title' in task_admin.list_display
    assert 'status' in task_admin.list_display
    assert 'priority' in task_admin.list_display
    assert 'due_date' in task_admin.list_display

    category_admin = site._registry[Category]
    assert 'name' in category_admin.list_display
    assert 'created_at' in category_admin.list_display


@pytest.mark.django_db
def test_admin_search_fields():
    task_admin = site._registry[Task]
    assert 'title' in task_admin.search_fields
    assert 'description' in task_admin.search_fields


@pytest.mark.django_db
def test_admin_ordering():
    task_admin = site._registry[Task]
    # ordering is a tuple, not a list
    assert task_admin.ordering == ('-created_at',)
