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
        user = User.objects.create_user(username="testuser", password="testpass")
        form = TaskForm(data={"title": "Test", "priority": None}, user=user)
        assert not form.is_valid()
        assert "priority" in form.errors

    def test_form_save_with_user_from_instance(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        form = TaskForm(
            data={
                "title": "Test",
                "priority": "medium",
                "status": "pending",
                "category_name": "New Category",
            },
            user=user,
        )
        assert form.is_valid()
        task = form.save(commit=False)
        task.user = user
        task.save()
        assert Category.objects.filter(name="New Category", user=user).exists()

    def test_form_save_without_commit(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        form = TaskForm(
            data={"title": "Test", "priority": "medium", "status": "pending"}, user=user
        )
        assert form.is_valid()
        task = form.save(commit=False)
        task.user = user
        assert task.pk is None
        task.save()
        assert task.pk is not None
