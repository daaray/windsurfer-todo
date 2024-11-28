import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from todos.models import Todo

@pytest.mark.django_db
class TestTodoViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def todo_data(self):
        return {
            "title": "Test Todo",
            "completed": False
        }

    def test_create_todo(self, api_client, todo_data):
        """Test creating a todo via API"""
        url = reverse('todo-list')
        response = api_client.post(url, todo_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Todo.objects.count() == 1
        assert Todo.objects.get().title == todo_data['title']
        assert response.data['order'] == 1  # First todo should have order 1

    def test_list_todos(self, api_client):
        """Test listing todos"""
        Todo.objects.create(title="Todo 1", order=1)
        Todo.objects.create(title="Todo 2", order=2)

        url = reverse('todo-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_retrieve_todo(self, api_client):
        """Test retrieving a specific todo"""
        todo = Todo.objects.create(title="Test Todo", order=1)
        
        url = reverse('todo-detail', kwargs={'pk': todo.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == todo.title

    def test_update_todo(self, api_client):
        """Test updating a todo"""
        todo = Todo.objects.create(title="Original Title", order=1)
        
        url = reverse('todo-detail', kwargs={'pk': todo.pk})
        updated_data = {
            "title": "Updated Title",
            "completed": True
        }
        response = api_client.patch(url, updated_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        todo.refresh_from_db()
        assert todo.title == updated_data['title']
        assert todo.completed == updated_data['completed']

    def test_delete_todo(self, api_client):
        """Test deleting a todo"""
        todo = Todo.objects.create(title="Test Todo", order=1)
        
        url = reverse('todo-detail', kwargs={'pk': todo.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Todo.objects.count() == 0

    def test_reorder_todos(self, api_client):
        """Test reordering todos"""
        todo1 = Todo.objects.create(title="Todo 1", order=1)
        todo2 = Todo.objects.create(title="Todo 2", order=2)
        
        url = reverse('todo-reorder')
        reorder_data = [
            {"id": todo1.id, "order": 2},
            {"id": todo2.id, "order": 1}
        ]
        response = api_client.post(url, reorder_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        todo1.refresh_from_db()
        todo2.refresh_from_db()
        assert todo1.order == 2
        assert todo2.order == 1

    def test_reorder_invalid_data(self, api_client):
        """Test reordering with invalid data"""
        url = reverse('todo-reorder')
        
        # Test with non-list data
        response = api_client.post(url, {"not": "a list"}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Test with invalid todo id
        response = api_client.post(url, [{"id": 999, "order": 1}], format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Test with missing required fields
        response = api_client.post(url, [{"id": 1}], format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
