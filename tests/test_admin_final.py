"""
Final tests to cover remaining lines in admin.py.
"""
import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from tasks.admin import TaskAdmin, CategoryAdmin
from tasks.models import Task, Category
from django.test import RequestFactory
from django.contrib.admin.sites import AdminSite


@pytest.mark.django_db
def test_admin_get_actions():
    """Test that admin has default actions."""
    task_admin = site._registry[Task]
    # Admin should have default actions like delete_selected
    actions = task_admin.get_actions(None)
    assert 'delete_selected' in actions


@pytest.mark.django_db
def test_admin_get_search_results():
    """Test admin search functionality."""
    user = User.objects.create_user(username='testuser', password='testpass')
    task_admin = site._registry[Task]
    request = RequestFactory().get('/admin/tasks/task/')
    request.user = user
    queryset = Task.objects.all()
    # Test that search doesn't raise exceptions
    search_results, use_distinct = task_admin.get_search_results(request, queryset, 'test')
    assert use_distinct is False
