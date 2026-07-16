from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task API.
    """

    user = serializers.ReadOnlyField(
        source="user.username",
    )

    class Meta:
        model = Task
        fields = "__all__"

        read_only_fields = (
            "id",
            "user",
            "created_at",
            "updated_at",
        )
