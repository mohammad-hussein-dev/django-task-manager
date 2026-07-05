"""
Final tests to cover remaining lines in views.py.
"""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from tasks.models import Task, Category


@pytest.mark.django_db
class TestTaskViewsFinal:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = Client()

    def test_task_list_pagination_with_filters(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        for i in range(15):
            Task.objects.create(title=f'Task {i}', user=user)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks:task_list') + '?page=2')
        assert response.status_code == 200
        assert 'Task 10' in str(response.content)

    def test_task_list_with_invalid_page(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        Task.objects.create(title='Test Task', user=user)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks:task_list') + '?page=abc')
        assert response.status_code == 200
        assert response.context['page_obj'].number == 1

    def test_task_list_with_out_of_range_page(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        for i in range(5):
            Task.objects.create(title=f'Task {i}', user=user)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks:task_list') + '?page=999')
        assert response.status_code == 200
        assert response.context['page_obj'].number == 1

    def test_task_list_with_category_filter_empty(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        category = Category.objects.create(name='Work', user=user)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks:task_list') + f'?category={category.id}')
        assert response.status_code == 200
        assert 'No tasks found' in str(response.content)

    def test_task_detail_view_with_other_user(self):
        user1 = User.objects.create_user(username='user1', password='testpass')
        user2 = User.objects.create_user(username='user2', password='testpass')
        task = Task.objects.create(title='Secret', user=user1)
        self.client.login(username='user2', password='testpass')
        response = self.client.get(reverse('tasks:task_detail', args=[task.pk]))
        assert response.status_code == 404

    def test_task_update_view_with_other_user(self):
        user1 = User.objects.create_user(username='user1', password='testpass')
        user2 = User.objects.create_user(username='user2', password='testpass')
        task = Task.objects.create(title='Secret', user=user1)
        self.client.login(username='user2', password='testpass')
        response = self.client.get(reverse('tasks:task_update', args=[task.pk]))
        assert response.status_code == 404

    def test_task_delete_view_with_other_user(self):
        user1 = User.objects.create_user(username='user1', password='testpass')
        user2 = User.objects.create_user(username='user2', password='testpass')
        task = Task.objects.create(title='Secret', user=user1)
        self.client.login(username='user2', password='testpass')
        response = self.client.get(reverse('tasks:task_delete', args=[task.pk]))
        assert response.status_code == 404

    def test_task_toggle_with_other_user(self):
        user1 = User.objects.create_user(username='user1', password='testpass')
        user2 = User.objects.create_user(username='user2', password='testpass')
        task = Task.objects.create(title='Secret', user=user1)
        self.client.login(username='user2', password='testpass')
        response = self.client.get(reverse('tasks:task_toggle', args=[task.pk]))
        assert response.status_code == 404
