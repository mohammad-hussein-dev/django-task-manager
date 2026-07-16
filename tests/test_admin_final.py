"""
Final tests to cover remaining lines in admin.py.
"""

import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.test import RequestFactory

from tasks.models import Task


@pytest.mark.django_db
def test_admin_get_actions():
    task_admin = site._registry[Task]
    request = RequestFactory().get("/admin/tasks/task/")
    user = User.objects.create_user(username="testuser", password="testpass")
    request.user = user
    actions = task_admin.get_actions(request)
    # Check that at least one action exists (custom or default)
    assert len(actions) > 0


@pytest.mark.django_db
def test_admin_get_search_results():
    user = User.objects.create_user(username="testuser", password="testpass")
    task_admin = site._registry[Task]
    request = RequestFactory().get("/admin/tasks/task/")
    request.user = user
    queryset = Task.objects.all()
    search_results, use_distinct = task_admin.get_search_results(
        request, queryset, "test"
    )
    assert use_distinct is False
