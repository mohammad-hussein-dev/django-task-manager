from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers import TaskSerializer
from tasks.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Task model.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Task.objects.filter(user=self.request.user)
            .select_related("category")
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
