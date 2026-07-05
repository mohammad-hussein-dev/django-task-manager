"""
Test to cover line 69 in forms.py (category_name initial value when editing).
"""
import pytest
from django.contrib.auth.models import User
from tasks.forms import TaskForm
from tasks.models import Category, Task


@pytest.mark.django_db
def test_form_edit_with_category():
    """Cover line 69: when editing a task that has a category."""
    user = User.objects.create_user(username='testuser', password='testpass')
    category = Category.objects.create(name='Work', user=user)
    task = Task.objects.create(title='Test', user=user, category=category)
    
    # Creating form with instance should set category_name initial value
    form = TaskForm(instance=task, user=user)
    # This will execute line 69: self.fields["category_name"].initial = self.instance.category.name
    assert form.fields['category_name'].initial == 'Work'
    
    
@pytest.mark.django_db
def test_form_edit_without_category():
    """Test that category_name initial is empty when task has no category."""
    user = User.objects.create_user(username='testuser', password='testpass')
    task = Task.objects.create(title='Test', user=user)
    
    form = TaskForm(instance=task, user=user)
    # Line 69 should not be executed (no category), so initial should be empty
    assert form.fields['category_name'].initial == ''
