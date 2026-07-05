"""
Test to cover remaining line in views.py (priority filter edge case).
"""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from tasks.models import Task


@pytest.mark.django_db
def test_priority_filter_without_query_param():
    """Test that priority filter works without any priority parameter."""
    user = User.objects.create_user(username='testuser', password='testpass')
    Task.objects.create(title='High Task', user=user, priority='high')
    client = Client()
    client.login(username='testuser', password='testpass')
    response = client.get(reverse('tasks:task_list'))  # No priority filter
    assert response.status_code == 200
    assert 'High Task' in response.content.decode()
