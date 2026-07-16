"""
Test to cover line 94 in forms.py (category set to None when category_name is empty and user is None).
"""

import pytest

from tasks.forms import TaskForm


@pytest.mark.django_db
def test_forms_line_94():
    """
    Cover line 94: when category_name is empty and user is None,
    instance.category should be set to None.
    """
    # Create a form without user and with empty category_name
    form = TaskForm(
        data={
            "title": "Test Task",
            "priority": "medium",
            "status": "pending",
            "category_name": "",  # empty
        }
    )
    assert form.is_valid()
    task = form.save(commit=False)
    # This should execute line 94: instance.category = None
    assert task.category is None
