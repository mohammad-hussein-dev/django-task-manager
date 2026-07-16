from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from tasks.forms import TaskForm
from tasks.models import Task


class Final100CoverageTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="coverage100",
            password="password123",
        )

        self.client = Client()

        self.client.login(
            username="coverage100",
            password="password123",
        )

    def test_api_perform_create_line_24(self):
        api_client = APIClient()

        api_client.force_authenticate(user=self.user)

        response = api_client.post(
            "/api/tasks/",
            {
                "title": "API Created Task",
                "description": "coverage",
                "priority": "high",
                "status": "pending",
            },
            format="json",
        )

        self.assertIn(
            response.status_code,
            [200, 201],
        )

        self.assertTrue(
            Task.objects.filter(
                user=self.user,
                title="API Created Task",
            ).exists()
        )

    def test_form_commit_true_lines_99_100(self):
        form = TaskForm(
            data={
                "title": "Commit True",
                "description": "coverage",
                "priority": "medium",
                "status": "pending",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid())

        form.instance.user = self.user

        task = form.save()

        self.assertEqual(
            task.user,
            self.user,
        )

    def test_task_create_form_valid_lines_168_169(self):
        response = self.client.post(
            reverse("tasks:task_create"),
            {
                "title": "Created From View",
                "description": "coverage",
                "priority": "low",
                "status": "pending",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            Task.objects.filter(
                user=self.user,
                title="Created From View",
            ).exists()
        )
