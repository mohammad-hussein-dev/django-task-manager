"""
Ultimate test to cover line 94 in forms.py with commit=True.
"""
import pytest
from django.contrib.auth.models import User
from tasks.forms import TaskForm
from tasks.models import Category, Task


@pytest.mark.django_db
def test_forms_line_94_ultimate():
    """
    Cover line 94: when category_name is empty but user exists.
    This ensures the else branch executes with commit=True.
    """
    user = User.objects.create_user(username='testuser', password='testpass')
    
    # Form with user and empty category_name
    form = TaskForm(data={
        'title': 'Ultimate Test',
        'priority': 'medium',
        'status': 'pending',
        'category_name': ''  # empty, triggers the else branch
    }, user=user)
    
    assert form.is_valid()
    task = form.save()  # commit=True
    
    # Line 94 should have executed: instance.category = None
    assert task.category is None
    assert task.user == user
