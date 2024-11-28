import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useTodos } from '../useTodos';
import axios from 'axios';

// Mock axios before tests
vi.mock('axios');

// Mock Quasar Notify
vi.mock('quasar', () => ({
  Notify: {
    create: vi.fn(),
  },
}));

describe('useTodos', () => {
  const mockTodos = [
    { id: 1, title: 'Test Todo 1', completed: false, order: 1 },
    { id: 2, title: 'Test Todo 2', completed: true, order: 2 },
  ];

  beforeEach(() => {
    // Reset all mocks before each test
    vi.clearAllMocks();

    // Setup default successful response
    axios.get.mockResolvedValue({ data: mockTodos });
    axios.post.mockResolvedValue({ data: mockTodos[0] });
    axios.patch.mockResolvedValue({ data: mockTodos[0] });
    axios.delete.mockResolvedValue({});
  });

  it('fetches todos', async () => {
    const { todos, fetchTodos } = useTodos();
    await fetchTodos();

    expect(axios.get).toHaveBeenCalledWith('/api/todos/');
    expect(todos.value).toEqual(mockTodos);
  });

  it('adds a new todo', async () => {
    const { addTodo } = useTodos();
    const newTodoTitle = 'New Todo';

    await addTodo(newTodoTitle);

    expect(axios.post).toHaveBeenCalledWith('/api/todos/', {
      title: newTodoTitle,
      completed: false,
    });
  });

  it('toggles a todo', async () => {
    const { toggleTodo } = useTodos();
    const todo = { ...mockTodos[0], completed: false };

    await toggleTodo(todo);

    expect(axios.patch).toHaveBeenCalledWith(`/api/todos/${todo.id}/`, {
      completed: true,
    });
  });

  it('deletes a todo', async () => {
    const { deleteTodo } = useTodos();
    const todo = mockTodos[0];

    await deleteTodo(todo);

    expect(axios.delete).toHaveBeenCalledWith(`/api/todos/${todo.id}/`);
  });

  it('reorders todos', async () => {
    const { reorderTodos } = useTodos();
    const newOrder = mockTodos.map((todo, index) => ({
      id: todo.id,
      order: index + 1,
    }));

    await reorderTodos(newOrder);

    expect(axios.post).toHaveBeenCalledWith('/api/todos/reorder/', newOrder);
  });

  it('handles API errors gracefully', async () => {
    const error = new Error('API Error');
    axios.get.mockRejectedValue(error);

    const { todos, fetchTodos } = useTodos();
    await fetchTodos();

    expect(todos.value).toEqual([]);
  });
});
