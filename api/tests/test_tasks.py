from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="apiuser",
            password="StrongPassword123!",
        )
