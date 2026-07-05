"""
Final tests to cover remaining lines in models.py.
"""
import pytest
from django.contrib.auth.models import User
from tasks.models import Category, Task


@pytest.mark.django_db
def test_category_str_method():
    user = User.objects.create_user(username='testuser', password='testpass')
    category = Category.objects.create(name='Test Category', user=user)
    assert str(category) == 'Test Category'


@pytest.mark.django_db
def test_task_str_method():
    user = User.objects.create_user(username='testuser', password='testpass')
    task = Task.objects.create(title='Test Task', user=user)
    assert str(task) == 'Test Task'


@pytest.mark.django_db
def test_category_meta_options():
    user = User.objects.create_user(username='testuser', password='testpass')
    Category.objects.create(name='Work', user=user)
    with pytest.raises(Exception):
        Category.objects.create(name='Work', user=user)
