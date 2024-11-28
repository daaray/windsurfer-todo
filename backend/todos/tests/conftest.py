import pytest
from rest_framework.test import APIClient
from django.core.management import call_command
from todos.models import Todo

@pytest.fixture(autouse=True)
def setup_database():
    """Set up the test database with migrations before each test"""
    call_command('migrate')
    yield
    call_command('flush', '--no-input')

@pytest.fixture
def api_client():
    """Create a test API client"""
    return APIClient()

@pytest.fixture
def todo_data():
    """Create test todo data"""
    return {
        'title': 'Test Todo',
        'completed': False
    }

@pytest.fixture
def sample_todo():
    """Create and return a sample todo"""
    return Todo.objects.create(
        title="Sample Todo",
        completed=False,
        order=1
    )

@pytest.fixture
def multiple_todos():
    """Create and return multiple todos"""
    todos = [
        Todo.objects.create(title=f"Todo {i}", order=i)
        for i in range(1, 4)
    ]
    return todos
