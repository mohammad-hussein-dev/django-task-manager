"""
Tests to cover missing lines in views.py.
"""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task, Category


@pytest.mark.django_db
class TestTaskViewsCoverage:
    def test_task_list_with_search_empty(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks:task_list') + '?search=nonexistent')
        assert response.status_code == 200
        assert 'No tasks found' in str(response.content)

    def test_task_list_with_priority_filter(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        Task.objects.create(title='High Task', user=user, priority='high')
        Task.objects.create(title='Low Task', user=user, priority='low')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks:task_list') + '?priority=high')
        assert response.status_code == 200
        assert 'High Task' in str(response.content)
        assert 'Low Task' not in str(response.content)

    def test_task_list_with_status_filter(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        Task.objects.create(title='Pending Task', user=user, status='pending')
        Task.objects.create(title='Completed Task', user=user, status='completed')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks:task_list') + '?status=completed')
        assert response.status_code == 200
        assert 'Completed Task' in str(response.content)
        assert 'Pending Task' not in str(response.content)

    def test_task_toggle_get_redirects(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        task = Task.objects.create(title='Test', user=user, status='pending')
        self.client.login(username='testuser', password='testpass')
        # Should redirect after toggle
        response = self.client.get(reverse('tasks:task_toggle', args=[task.pk]))
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.status == 'completed'

    def test_task_create_view_post_invalid_data(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('tasks:task_create'), {
            'title': '',
            'priority': 'invalid'
        })
        assert response.status_code == 200
        assert response.context['form'].errors

    def test_task_update_view_post_invalid_data(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        task = Task.objects.create(title='Test', user=user)
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('tasks:task_update', args=[task.pk]), {
            'title': '',
            'priority': 'invalid'
        })
        assert response.status_code == 200
        assert response.context['form'].errors

    def test_task_delete_view_get(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        task = Task.objects.create(title='Test', user=user)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks:task_delete', args=[task.pk]))
        assert response.status_code == 200
        # Check that it shows confirmation page (optional)
        assert 'Delete' in str(response.content)
