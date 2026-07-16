"""
Test to cover line 219 in views.py (search filter).
"""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from tasks.models import Task


@pytest.mark.django_db
def test_search_with_empty_string():
    """Cover line 219: if search is empty string, should not filter."""
    user = User.objects.create_user(username="testuser", password="testpass")
    Task.objects.create(title="Important Task", user=user)
    client = Client()
    client.login(username="testuser", password="testpass")
    response = client.get(reverse("tasks:task_list") + "?search=")
    assert response.status_code == 200
    # همه taskها باید نمایش داده شوند
    assert "Important Task" in response.content.decode()
