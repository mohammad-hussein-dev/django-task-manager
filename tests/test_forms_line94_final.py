"""
Final test to cover line 94 in forms.py (category set to None when category_name is empty).
"""

import pytest

from tasks.forms import TaskForm


@pytest.mark.django_db
def test_forms_line_94_final():
    """
    Cover line 94: when category_name is empty (or None) and user is None,
    instance.category should be set to None.
    """
    # Create a form without user and with category_name = None (not provided)
    form = TaskForm(
        data={
            "title": "Test Task",
            "priority": "medium",
            "status": "pending",
            # category_name is intentionally omitted (None)
        }
    )
    assert form.is_valid()
    task = form.save(commit=False)
    # This should execute line 94 (else clause): instance.category = None
    assert task.category is None

    # Also test with empty string explicitly
    form2 = TaskForm(
        data={
            "title": "Test Task 2",
            "priority": "low",
            "status": "pending",
            "category_name": "",  # empty string
        }
    )
    assert form2.is_valid()
    task2 = form2.save(commit=False)
    assert task2.category is None
