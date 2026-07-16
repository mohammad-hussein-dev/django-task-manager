from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from tasks.models import Task

User = get_user_model()


class TaskAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="apiuser",
            password="StrongPassword123!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="StrongPassword123!",
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Initial description",
            priority="medium",
            status="pending",
        )

    def test_list_tasks(self):

        response = self.client.get(
            reverse("task-list"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        if isinstance(response.data, dict):
            count = len(response.data["results"])
        else:
            count = len(response.data)

        self.assertEqual(
            count,
            1,
        )

    def test_create_task(self):

        response = self.client.post(
            reverse("task-list"),
            {
                "title": "New Task",
                "description": "Created from API",
                "priority": "high",
                "status": "pending",
                "category": None,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Task.objects.last().user,
            self.user,
        )

    def test_retrieve_task(self):

        response = self.client.get(
            reverse(
                "task-detail",
                args=[self.task.id],
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_task(self):

        response = self.client.put(
            reverse(
                "task-detail",
                args=[self.task.id],
            ),
            {
                "title": "Updated Task",
                "description": "Updated",
                "priority": "high",
                "status": "completed",
                "category": None,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_partial_update_task(self):

        response = self.client.patch(
            reverse(
                "task-detail",
                args=[self.task.id],
            ),
            {
                "status": "completed",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_task(self):

        response = self.client.delete(
            reverse(
                "task-detail",
                args=[self.task.id],
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_user_isolation(self):

        other_task = Task.objects.create(
            user=self.other_user,
            title="Private Task",
        )

        response = self.client.get(
            reverse(
                "task-detail",
                args=[other_task.id],
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
