"""
Final test to cover lines 69 and 94 in forms.py.
"""
import pytest
from django.contrib.auth.models import User
from tasks.forms import TaskForm
from tasks.models import Category, Task


@pytest.mark.django_db
def test_forms_line_69_and_94():
    """
    - Line 69: when editing a task with category, category_name.initial is set.
    - Line 94: when category_name is empty and user is None, category is set to None.
    """
    user = User.objects.create_user(username='testuser', password='testpass')
    category = Category.objects.create(name='Work', user=user)
    task = Task.objects.create(title='Test', user=user, category=category)

    # --- Line 69: Edit with category ---
    form = TaskForm(instance=task, user=user)
    assert form.fields['category_name'].initial == 'Work'

    # --- Line 94: Save with empty category_name and no user ---
    form2 = TaskForm(data={
        'title': 'Test 2',
        'priority': 'medium',
        'status': 'pending',
        'category_name': ''  # empty
    })
    assert form2.is_valid()
    task2 = form2.save(commit=False)
    # This should execute line 94: instance.category = None
    assert task2.category is None
