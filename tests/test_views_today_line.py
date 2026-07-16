from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Task


class TodayFilterCoverage(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="todaycoverage",
            password="password123",
        )

        self.client = Client()

        self.client.login(
            username="todaycoverage",
            password="password123",
        )

    def test_task_list_today_filter_line_67(self):
        Task.objects.create(
            user=self.user,
            title="Today Task",
            due_date=date.today(),
        )

        response = self.client.get(
            reverse("tasks:task_list"),
            {
                "date_filter": "today",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )
