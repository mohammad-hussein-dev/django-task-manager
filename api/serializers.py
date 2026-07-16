from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
