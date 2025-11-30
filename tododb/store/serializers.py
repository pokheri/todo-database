from rest_framework.serializers import ModelSerializer
from core.models import Tasks


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Tasks
        fields = ["user", "title", "description", "id"]
        read_only_fields = ["id"]
        extra_kwargs = {"user": {"write_only": True}}
