import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { ref } from 'vue';

// Create mock variables in the outer scope
const mockTodos = ref([]);
const mockFetchTodos = vi.fn();
const mockAddTodo = vi.fn();
const mockToggleTodo = vi.fn();
const mockDeleteTodo = vi.fn();
const mockReorderTodos = vi.fn();

vi.mock('../../composables/useTodos', () => ({
  useTodos: () => ({
    todos: mockTodos,
    fetchTodos: mockFetchTodos,
    addTodo: mockAddTodo,
    toggleTodo: mockToggleTodo,
    deleteTodo: mockDeleteTodo,
    reorderTodos: mockReorderTodos,
  }),
}));

vi.mock('quasar', () => ({
  Quasar: {
    install: vi.fn(),
  },
  Notify: {
    create: vi.fn(),
  },
  Ripple: {
    mounted: vi.fn(),
    unmounted: vi.fn(),
  },
  QInput: {
    name: 'QInput',
    template:
      '<div class="q-input todo-input"><input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" @keyup.enter="$emit(\'keyup.enter\')" /><slot name="append" /></div>',
    props: ['modelValue'],
    emits: ['update:modelValue', 'keyup.enter'],
  },
  QItem: {
    name: 'QItem',
    template: '<div class="q-item todo-item" :class="$attrs.class"><slot /></div>',
  },
  QItemSection: {
    name: 'QItemSection',
    template: '<div class="q-item-section" :class="{ avatar: avatar, side: side }"><slot /></div>',
    props: ['avatar', 'side'],
  },
  QItemLabel: {
    name: 'QItemLabel',
    template: '<div class="q-item-label" :class="$attrs.class"><slot /></div>',
  },
  QCheckbox: {
    name: 'QCheckbox',
    template:
      '<div class="q-checkbox todo-checkbox"><input type="checkbox" :checked="modelValue" @change="$emit(\'update:modelValue\', $event.target.checked)" /></div>',
    props: ['modelValue'],
    emits: ['update:modelValue'],
  },
  QBtn: {
    name: 'QBtn',
    template:
      '<button class="q-btn" :class="$attrs.class" @click="$emit(\'click\')"><slot /></button>',
    props: ['flat', 'round', 'dense', 'icon', 'color'],
    emits: ['click'],
  },
}));

// Mock draggable component
const MockDraggable = {
  name: 'draggable',
  template: `
    <div class="draggable-container">
      <template v-for="(item, index) in modelValue" :key="item.id">
        <slot name="item" :element="item" :index="index"></slot>
      </template>
    </div>
  `,
  props: ['modelValue', 'itemKey'],
  emits: ['update:modelValue', 'end'],
};

// Import component after mocks
import TodoList from '../TodoList.vue';

describe('TodoList.vue', () => {
  let wrapper;

  beforeEach(() => {
    // Reset the mocked todos and functions before each test
    mockTodos.value = [];
    vi.clearAllMocks();

    wrapper = mount(TodoList, {
      global: {
        components: {
          draggable: MockDraggable,
        },
      },
    });
  });

  it('renders the todo list', () => {
    expect(wrapper.find('.todo-list').exists()).toBe(true);
  });

  it('displays the add todo input', () => {
    expect(wrapper.find('.todo-input').exists()).toBe(true);
  });

  it('can add a new todo', async () => {
    const input = wrapper.find('.todo-input input');
    await input.setValue('New Todo');
    await input.trigger('keyup.enter');

    expect(wrapper.vm.newTodo).toBe('');
    expect(mockAddTodo).toHaveBeenCalledWith('New Todo');
  });

  it('can mark a todo as complete', async () => {
    // Set the mock todos
    mockTodos.value = [
      {
        id: 1,
        title: 'Test Todo',
        completed: false,
        order: 1,
      },
    ];

    await wrapper.vm.$nextTick();
    await flushPromises();

    const todoItem = wrapper.find('.todo-item');
    expect(todoItem.exists()).toBe(true);

    const checkbox = todoItem.findComponent({ name: 'QCheckbox' });
    expect(checkbox.exists()).toBe(true);

    await checkbox.vm.$emit('update:modelValue', true);
    expect(mockToggleTodo).toHaveBeenCalledWith(mockTodos.value[0]);
  });

  it('can delete a todo', async () => {
    // Set the mock todos
    mockTodos.value = [
      {
        id: 1,
        title: 'Test Todo',
        completed: false,
        order: 1,
      },
    ];

    await wrapper.vm.$nextTick();
    await flushPromises();

    const todoItem = wrapper.find('.todo-item');
    expect(todoItem.exists()).toBe(true);

    const deleteBtn = todoItem.find('.delete-todo');
    expect(deleteBtn.exists()).toBe(true);

    await deleteBtn.trigger('click');
    expect(mockDeleteTodo).toHaveBeenCalledWith(mockTodos.value[0]);
  });

  it('can reorder todos', async () => {
    mockTodos.value = [
      { id: 1, title: 'First Todo', completed: false, order: 1 },
      { id: 2, title: 'Second Todo', completed: false, order: 2 },
    ];
    await wrapper.vm.$nextTick();
    await flushPromises();

    // Simulate drag and drop
    await wrapper.vm.onDragEnd({
      oldIndex: 0,
      newIndex: 1,
    });

    expect(mockReorderTodos).toHaveBeenCalled();
  });
});
