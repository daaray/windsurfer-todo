"""Serializers for Todo application."""

from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for Todo model."""

    class Meta:
        """Meta options for TodoSerializer."""

        model = Todo
        fields = [
            "id",
            "title",
            "completed",
            "order",
            "created_at",
            "updated_at",
        ]
