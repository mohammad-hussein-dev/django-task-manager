from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Task


class LastLineCoverage(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="lastcoverage",
            password="password123",
        )

        self.client = Client()

        self.client.login(
            username="lastcoverage",
            password="password123",
        )

    def test_task_list_this_week_branch_full(self):
        Task.objects.create(
            user=self.user,
            title="This Week",
            due_date=date.today(),
        )

        response = self.client.get(
            reverse("tasks:task_list"),
            {
                "date_filter": "this_week",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )
