"""Test cases for Todo views."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Todo


@pytest.mark.django_db
class TestTodoViewSet:
    """Test cases for TodoViewSet."""

    @pytest.fixture
    def api_client(self):
        """Return an API client for testing."""
        return APIClient()

    @pytest.fixture
    def todo_data(self):
        """Return test todo data."""
        return {"title": "Test Todo", "completed": False}

    def test_list_todos(self, api_client, todo_factory):
        """Test listing todos returns expected data."""
        todo_factory.create_batch(3)
        response = api_client.get(reverse("todo-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_todo(self, api_client):
        """Test creating a todo with valid data."""
        data = {"title": "Test Todo", "completed": False}
        response = api_client.post(reverse("todo-list"), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Todo.objects.count() == 1
        assert Todo.objects.first().title == "Test Todo"

    def test_update_todo(self, api_client, todo_factory):
        """Test updating a todo's title and completion status."""
        todo = todo_factory()
        data = {"title": "Updated Todo", "completed": True}
        response = api_client.put(reverse("todo-detail", args=[todo.id]), data)
        assert response.status_code == status.HTTP_200_OK
        todo.refresh_from_db()
        assert todo.title == "Updated Todo"
        assert todo.completed is True

    def test_delete_todo(self, api_client, todo_factory):
        """Test deleting a todo removes it from database."""
        todo = todo_factory()
        response = api_client.delete(reverse("todo-detail", args=[todo.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Todo.objects.filter(id=todo.id).exists()

    def test_reorder_todos(self, api_client, todo_factory):
        """Test reordering todos updates their order field correctly."""
        todos = todo_factory.create_batch(3)
        data = [
            {"id": todos[0].id, "order": 2},
            {"id": todos[1].id, "order": 0},
            {"id": todos[2].id, "order": 1},
        ]
        response = api_client.post(reverse("todo-reorder"), data)
        assert response.status_code == status.HTTP_200_OK

        # Verify new orders
        todos[0].refresh_from_db()
        todos[1].refresh_from_db()
        todos[2].refresh_from_db()
        assert todos[0].order == 2
        assert todos[1].order == 0
        assert todos[2].order == 1
