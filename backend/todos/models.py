"""Models for Todo application."""

from django.db import models


class Todo(models.Model):
    """Model representing a todo item."""

    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for Todo model."""

        ordering = ["order", "id"]

    def __str__(self):
        """Return string representation of todo."""
        return self.title
