"""Test cases for Todo models."""

import pytest
from django.utils import timezone

from ..models import Todo


@pytest.mark.django_db
class TestTodoModel:
    """Test cases for Todo model."""

    def test_create_todo(self):
        """Test creating a todo with basic attributes."""
        todo = Todo.objects.create(title="Test Todo", completed=False, order=1)
        assert todo.title == "Test Todo"
        assert todo.completed is False
        assert todo.order == 1
        assert isinstance(todo.created_at, timezone.datetime)
        assert isinstance(todo.updated_at, timezone.datetime)

    def test_todo_str_representation(self):
        """Test string representation of todo."""
        todo = Todo.objects.create(title="Test Todo")
        assert str(todo) == "Test Todo"

    def test_todo_ordering(self):
        """Test todos are ordered by order field and then by id."""
        # Create todos in different order
        todo2 = Todo.objects.create(title="Second", order=1)
        todo3 = Todo.objects.create(title="Third", order=2)
        todo1 = Todo.objects.create(title="First", order=1)

        todos = list(Todo.objects.all())
        # Should be ordered by order first, then by id
        assert todos[0] == todo2  # order=1, created first
        assert todos[1] == todo1  # order=1, created last
        assert todos[2] == todo3  # order=2

    def test_todo_defaults(self):
        """Test default values for todo fields."""
        todo = Todo.objects.create(title="Test Todo")
        assert todo.completed is False
        assert todo.order == 0
