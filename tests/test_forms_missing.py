"""
Tests to cover lines 69 and 94 in forms.py.
"""

import pytest
from django.contrib.auth.models import User

from tasks.forms import TaskForm
from tasks.models import Category


@pytest.mark.django_db
def test_form_save_commit_false():
    """Cover line 69: when commit=False and then manually saved."""
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

    # خط 69: save(commit=False)
    task = form.save(commit=False)
    task.user = user
    assert task.pk is None  # هنوز ذخیره نشده
    task.save()  # ذخیره دستی
    assert task.pk is not None
    assert Category.objects.filter(name="New Category", user=user).exists()


@pytest.mark.django_db
def test_form_save_without_user_and_category_name():
    """Cover line 94: when category_name is empty and user is None."""
    # فرم بدون user و بدون category_name
    form = TaskForm(
        data={
            "title": "Test",
            "priority": "medium",
            "status": "pending",
            "category_name": "",
        }
    )
    assert form.is_valid()
    task = form.save(commit=False)
    # باید category را None تنظیم کند (خط 94)
    assert task.category is None
