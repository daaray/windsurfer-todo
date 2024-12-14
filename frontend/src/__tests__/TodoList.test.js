import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { QList, QItem, QItemSection, QCheckbox } from 'quasar';
import TodoList from '../components/TodoList.vue';
import { useTodos } from '../composables/useTodos';

// Mock draggable component
const MockDraggable = {
  name: 'draggable',
  template: `
    <div>
      <template v-for="item in modelValue" :key="item.id">
        <slot name="item" :element="item"></slot>
      </template>
    </div>
  `,
  props: ['modelValue'],
};

// Mock useTodos composable
vi.mock('../composables/useTodos', () => ({
  useTodos: vi.fn(() => ({
    todos: { value: [] },
    fetchTodos: vi.fn(),
    addTodo: vi.fn(),
    toggleTodo: vi.fn(),
    deleteTodo: vi.fn(),
    reorderTodos: vi.fn(),
  })),
}));

describe('TodoList', () => {
  const mountOptions = {
    global: {
      stubs: {
        QList,
        QItem,
        QItemSection,
        QCheckbox,
        QIcon: true,
        draggable: MockDraggable,
      },
    },
  };

  it('renders properly', () => {
    const wrapper = mount(TodoList, {
      props: {
        todos: [],
      },
      ...mountOptions,
    });
    expect(wrapper.exists()).toBe(true);
  });

  it('displays todos when provided', async () => {
    const todos = [
      { id: 1, title: 'Test Todo 1', completed: false },
      { id: 2, title: 'Test Todo 2', completed: true },
    ];

    // Mock the useTodos composable for this specific test
    vi.mocked(useTodos).mockReturnValue({
      todos: { value: todos },
      fetchTodos: vi.fn(),
      addTodo: vi.fn(),
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
      reorderTodos: vi.fn(),
    });

    const wrapper = mount(TodoList, mountOptions);
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick(); // Wait for another tick to ensure draggable updates

    const todoItems = wrapper.findAll('.todo-item');
    expect(todoItems).toHaveLength(2);
    expect(todoItems[0].text()).toContain('Test Todo 1');
    expect(todoItems[1].text()).toContain('Test Todo 2');
  });
});
