"""Fixtures for Todo app tests."""

import pytest
from rest_framework.test import APIClient

from ..models import Todo


@pytest.fixture
def api_client():
    """Create and return an API client for testing."""
    return APIClient()


@pytest.fixture
def todo_factory(db):
    """Create a factory function for Todo instances."""

    def create_todo(**kwargs):
        """Create and return a Todo instance with given kwargs."""
        defaults = {"title": "Test Todo", "completed": False, "order": 0}
        defaults.update(kwargs)
        return Todo.objects.create(**defaults)

    return create_todo
