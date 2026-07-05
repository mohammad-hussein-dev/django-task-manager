"""
Tests to cover missing lines in forms.py.
"""
import pytest
from django.contrib.auth.models import User
from tasks.forms import TaskForm
from tasks.models import Category, Task


@pytest.mark.django_db
class TestTaskFormCoverage:
    def test_form_init_with_user(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        user2 = User.objects.create_user(username='other', password='testpass')
        Category.objects.create(name='Work', user=user)
        Category.objects.create(name='Personal', user=user2)

        form = TaskForm(user=user)
        # Test that category_name field exists
        assert 'category_name' in form.fields

    def test_form_init_without_user(self):
        form = TaskForm()
        assert 'category_name' in form.fields

    def test_form_clean_priority_valid(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        form = TaskForm(data={
            'title': 'Test',
            'priority': 'low',
            'status': 'pending',
            'category_name': ''
        }, user=user)
        assert form.is_valid()

    def test_form_clean_priority_invalid(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        form = TaskForm(data={'title': 'Test', 'priority': 'invalid'}, user=user)
        assert not form.is_valid()
        assert 'priority' in form.errors

    def test_form_save_with_category_name(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        form = TaskForm(data={
            'title': 'Test Task',
            'priority': 'medium',
            'status': 'pending',
            'category_name': 'New Category'
        }, user=user)
        assert form.is_valid()
        task = form.save(commit=False)
        task.user = user
        task.save()
        assert Category.objects.filter(name='New Category', user=user).exists()
        assert task.category.name == 'New Category'

    def test_form_save_without_category_name(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        form = TaskForm(data={
            'title': 'Test Task',
            'priority': 'medium',
            'status': 'pending'
        }, user=user)
        assert form.is_valid()
        task = form.save(commit=False)
        task.user = user
        task.save()
        assert task.category is None
