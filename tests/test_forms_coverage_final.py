"""
Final tests to cover remaining lines in forms.py.
"""
import pytest
from django.contrib.auth.models import User
from tasks.forms import TaskForm
from tasks.models import Category, Task


@pytest.mark.django_db
def test_form_save_with_existing_category_name():
    """Test save with category_name that already exists (should use existing)."""
    user = User.objects.create_user(username='testuser', password='testpass')
    category = Category.objects.create(name='Work', user=user)
    
    form = TaskForm(data={
        'title': 'Test',
        'priority': 'medium',
        'status': 'pending',
        'category_name': 'Work'  # Already exists
    }, user=user)
    assert form.is_valid()
    task = form.save(commit=False)
    task.user = user
    task.save()
    # Should use the existing category, not create a new one
    assert Category.objects.filter(name='Work', user=user).count() == 1
    assert task.category == category


@pytest.mark.django_db
def test_form_save_with_user_as_none():
    """Test save when user is None (should handle gracefully)."""
    # فرم بدون user و با category_name معتبر
    form = TaskForm(data={
        'title': 'Test',
        'priority': 'medium',
        'status': 'pending',
        'category_name': 'Work'
    })
    assert form.is_valid()
    task = form.save(commit=False)
    # user باید None باشد و category هم None
    assert task.user is None
    assert task.category is None
