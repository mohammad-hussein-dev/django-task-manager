"""
Tests to cover missing lines in models.py.
"""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Category, Task


@pytest.mark.django_db
class TestCategoryModelCoverage:
    def test_category_get_absolute_url(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        category = Category.objects.create(name='Work', user=user)
        url = category.get_absolute_url()
        assert url == reverse('tasks:task_list') + f'?category={category.id}'

    def test_category_unique_together(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        Category.objects.create(name='Work', user=user)
        with pytest.raises(Exception):
            Category.objects.create(name='Work', user=user)


@pytest.mark.django_db
class TestTaskModelCoverage:
    def test_task_get_absolute_url(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        task = Task.objects.create(title='Test Task', user=user)
        url = task.get_absolute_url()
        assert url == reverse('tasks:task_detail', args=[task.pk])

    def test_task_default_values(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        task = Task.objects.create(title='Test', user=user)
        assert task.status == 'pending'
        assert task.priority == 'medium'
