from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from tasks.forms import TaskForm
from tasks.models import Category, Task


class RemainingCoverageTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="coverage",
            password="password123",
        )

        self.client = Client()

        self.client.login(
            username="coverage",
            password="password123",
        )

    def test_form_save_with_new_category_branch(self):

        form = TaskForm(
            data={
                "title": "Category Test",
                "description": "Test",
                "priority": "high",
                "status": "pending",
                "category_name": "New Category",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid())

        task = form.save(commit=False)

        task.user = self.user
        task.save()

        self.assertEqual(
            task.user,
            self.user,
        )

        self.assertTrue(Category.objects.filter(name="New Category").exists())

    def test_task_list_search_result_branch(self):

        Task.objects.create(
            user=self.user,
            title="Python Django",
        )

        url = reverse("tasks:task_list")

        response = self.client.get(
            url,
            {
                "search": "Python",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_toggle_completed_branch(self):

        task = Task.objects.create(
            user=self.user,
            title="Toggle",
            status="pending",
        )

        url = reverse(
            "tasks:task_toggle",
            kwargs={
                "pk": task.pk,
            },
        )

        response = self.client.get(url)

        self.assertIn(
            response.status_code,
            [200, 302],
        )

    def test_api_views_authenticated(self):

        api_client = APIClient()

        api_client.force_authenticate(user=self.user)

        response = api_client.get(
            "/api/tasks/",
        )

        self.assertNotEqual(
            response.status_code,
            401,
        )
