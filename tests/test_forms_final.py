"""
Final tests to cover remaining lines in forms.py.
"""
import pytest
from django.contrib.auth.models import User
from tasks.forms import TaskForm
from tasks.models import Category


@pytest.mark.django_db
class TestTaskFormFinal:
    def test_form_clean_priority_none(self):
        """Test that priority validation handles None value."""
        user = User.objects.create_user(username='testuser', password='testpass')
        form = TaskForm(data={'title': 'Test', 'priority': None}, user=user)
        assert not form.is_valid()
        assert 'priority' in form.errors

    def test_form_save_with_user_from_instance(self):
        """Test save when user comes from instance (edit scenario)."""
        user = User.objects.create_user(username='testuser', password='testpass')
        form = TaskForm(data={
            'title': 'Test',
            'priority': 'medium',
            'status': 'pending',
            'category_name': 'New Category'
        }, user=user)
        assert form.is_valid()
        task = form.save(commit=False)
        task.user = user
        task.save()
        # Test that category was created
        assert Category.objects.filter(name='New Category', user=user).exists()

    def test_form_save_without_commit(self):
        """Test save with commit=False."""
        user = User.objects.create_user(username='testuser', password='testpass')
        form = TaskForm(data={
            'title': 'Test',
            'priority': 'medium',
            'status': 'pending'
        }, user=user)
        assert form.is_valid()
        task = form.save(commit=False)
        task.user = user
        assert task.pk is None  # Not saved yet
        task.save()
        assert task.pk is not None  # Now saved
