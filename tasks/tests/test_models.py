from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Category, Task


class TaskModelTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="tester",
            password="password123",
        )

        self.category = Category.objects.create(
            user=self.user,
            name="Work",
        )

    def test_category_str(self):

        self.assertEqual(
            str(self.category),
            "Work",
        )

    def test_task_str(self):

        task = Task.objects.create(
            user=self.user,
            title="Testing",
        )

        self.assertEqual(
            str(task),
            "Testing",
        )

    def test_category_absolute_url(self):

        url = self.category.get_absolute_url()

        self.assertIn(
            "category",
            url,
        )

    def test_task_absolute_url(self):

        task = Task.objects.create(
            user=self.user,
            title="Testing",
        )

        url = task.get_absolute_url()

        self.assertEqual(
            url,
            reverse(
                "tasks:task_detail",
                kwargs={"pk": task.pk},
            ),
        )
