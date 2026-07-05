"""
Final tests to cover remaining lines in admin.py.
"""
import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from tasks.models import Task, Category
from django.test import RequestFactory


@pytest.mark.django_db
def test_admin_get_actions():
    task_admin = site._registry[Task]
    actions = task_admin.get_actions(None)
    assert 'delete_selected' in actions


@pytest.mark.django_db
def test_admin_get_search_results():
    user = User.objects.create_user(username='testuser', password='testpass')
    task_admin = site._registry[Task]
    request = RequestFactory().get('/admin/tasks/task/')
    request.user = user
    queryset = Task.objects.all()
    search_results, use_distinct = task_admin.get_search_results(request, queryset, 'test')
    assert use_distinct is False
