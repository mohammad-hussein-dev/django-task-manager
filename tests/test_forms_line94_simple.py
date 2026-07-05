"""
Ultra-simple test to cover line 94 in forms.py.
"""
import pytest
from tasks.forms import TaskForm


@pytest.mark.django_db
def test_forms_line_94_simple():
    """Directly test the else branch that sets category to None."""
    form = TaskForm(data={
        'title': 'Simple Task',
        'priority': 'medium',
        'status': 'pending',
        'category_name': ''  # empty string triggers the else branch
    })
    # فرم باید valid باشد تا save اجرا شود
    assert form.is_valid()
    
    # این خط باید خط 94 را اجرا کند
    task = form.save(commit=False)
    assert task.category is None
    
    # همچنین با commit=True تست کن
    task2 = form.save()
    assert task2.category is None
