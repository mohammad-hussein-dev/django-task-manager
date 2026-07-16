from django.test import TestCase

from tasks.forms import TaskForm


class TaskFormTests(TestCase):

    def test_valid_form(self):

        form = TaskForm(
            data={
                "title": "New task",
                "description": "Description",
                "priority": "high",
                "status": "pending",
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_form_without_title(self):

        form = TaskForm(data={})

        self.assertFalse(form.is_valid())
