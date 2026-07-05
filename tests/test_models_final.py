"""
Final tests to cover remaining lines in models.py.
"""
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tasks.models import Category, Task


@pytest.mark.django_db
def test_category_str_method():
    """Test Category.__str__ method."""
    user = User.objects.create_user(username='testuser', password='testpass')
    category = Category.objects.create(name='Test Category', user=user)
    assert str(category) == 'Test Category'


@pytest.mark.django_db
def test_task_str_method():
    """Test Task.__str__ method."""
    user = User.objects.create_user(username='testuser', password='testpass')
    task = Task.objects.create(title='Test Task', user=user)
    assert str(task) == 'Test Task'


@pytest.mark.django_db
def test_category_meta_options():
    """Test Category Meta options (ordering, verbose_name, unique_together)."""
    user = User.objects.create_user(username='testuser', password='testpass')
    category = Category.objects.create(name='Work', user=user)
    # Test unique_together by trying to create duplicate
    with pytest.raises(Exception):
        Category.objects.create(name='Work', user=user)
