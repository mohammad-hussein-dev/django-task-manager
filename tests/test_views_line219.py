"""
Test to cover line 219 in views.py (toggling completed task to pending).
"""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from tasks.models import Task


@pytest.mark.django_db
def test_toggle_completed_to_pending():
    """Cover line 219: when toggling a completed task back to pending."""
    user = User.objects.create_user(username='testuser', password='testpass')
    task = Task.objects.create(title='Test', user=user, status='completed')
    
    client = Client()
    client.login(username='testuser', password='testpass')
    response = client.get(reverse('tasks:task_toggle', args=[task.pk]))
    assert response.status_code == 302
    
    task.refresh_from_db()
    # Line 219: task.status = 'pending' should be executed
    assert task.status == 'pending'
