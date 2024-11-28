import pytest
from django.utils import timezone
from todos.models import Todo

@pytest.mark.django_db
class TestTodoModel:
    def test_create_todo(self):
        """Test creating a new todo item"""
        todo = Todo.objects.create(
            title="Test Todo",
            completed=False,
            order=1
        )
        assert todo.title == "Test Todo"
        assert todo.completed is False
        assert todo.order == 1
        assert isinstance(todo.created_at, timezone.datetime)
        assert isinstance(todo.updated_at, timezone.datetime)

    def test_todo_str_method(self):
        """Test the string representation of a todo"""
        todo = Todo.objects.create(
            title="Test Todo",
            completed=False,
            order=1
        )
        assert str(todo) == "Test Todo"

    def test_todo_ordering(self):
        """Test that todos are ordered by order field and then by created_at"""
        # Create todos in reverse order
        todo3 = Todo.objects.create(title="Todo 3", order=3)
        todo1 = Todo.objects.create(title="Todo 1", order=1)
        todo2 = Todo.objects.create(title="Todo 2", order=2)

        todos = Todo.objects.all()
        assert todos[0].title == "Todo 1"
        assert todos[1].title == "Todo 2"
        assert todos[2].title == "Todo 3"

    def test_todo_default_values(self):
        """Test the default values of a todo"""
        todo = Todo.objects.create(title="Test Todo")
        assert todo.completed is False
        assert todo.order == 0

    def test_todo_update(self):
        """Test updating a todo"""
        todo = Todo.objects.create(
            title="Original Title",
            completed=False,
            order=1
        )
        original_updated_at = todo.updated_at

        # Wait a moment to ensure updated_at will be different
        import time
        time.sleep(0.1)

        todo.title = "Updated Title"
        todo.completed = True
        todo.save()

        # Refresh from database
        todo.refresh_from_db()
        assert todo.title == "Updated Title"
        assert todo.completed is True
        assert todo.updated_at > original_updated_at
