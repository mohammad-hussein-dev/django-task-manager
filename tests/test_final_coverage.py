from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from tasks.forms import TaskForm
from tasks.models import Task


class FinalCoverageTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="finaluser",
            password="password123",
        )

        self.client = Client()

        self.client.login(
            username="finaluser",
            password="password123",
        )

    def test_form_save_without_category_name_lines(self):

        form = TaskForm(
            data={
                "title": "Coverage Task",
                "description": "Test",
                "priority": "medium",
                "status": "pending",
            }
        )

        self.assertTrue(form.is_valid())

        task = form.save(commit=False)

        task.user = self.user
        task.save()

        self.assertEqual(
            task.title,
            "Coverage Task",
        )

    def test_task_list_empty_search_branch(self):

        url = reverse("tasks:task_list")

        response = self.client.get(
            url,
            {
                "search": "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_task_create_invalid_branch(self):

        url = reverse("tasks:task_create")

        response = self.client.post(
            url,
            {
                "title": "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_task_update_invalid_branch(self):

        task = Task.objects.create(
            user=self.user,
            title="Old",
        )

        url = reverse(
            "tasks:task_update",
            kwargs={
                "pk": task.pk,
            },
        )

        response = self.client.post(
            url,
            {
                "title": "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_api_root_requires_authentication(self):

        response = self.client.get(
            "/api/",
        )

        self.assertEqual(
            response.status_code,
            401,
        )
