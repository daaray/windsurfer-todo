<template>
  <div class="todo-list q-pa-md">
    <q-input
      v-model="newTodo"
      class="todo-input q-mb-md"
      outlined
      dense
      placeholder="Add a new todo..."
      @keyup.enter="addNewTodo"
    >
      <template v-slot:append>
        <q-btn
          round
          dense
          flat
          icon="add"
          @click="addNewTodo"
        />
      </template>
    </q-input>

    <draggable
      v-model="sortableTodos"
      item-key="id"
      handle=".drag-handle"
      @end="onDragEnd"
    >
      <template #item="{ element: todo }">
        <q-item
          v-ripple
          class="todo-item q-mb-sm"
          :class="{ 'done': todo.completed }"
          bordered
        >
          <q-item-section avatar>
            <q-checkbox
              v-model="todo.completed"
              class="todo-checkbox"
              @update:model-value="toggleTodoComplete(todo)"
            />
          </q-item-section>

          <q-item-section>
            <q-item-label :class="{ 'text-strike': todo.completed }">
              {{ todo.title }}
            </q-item-label>
          </q-item-section>

          <q-item-section side>
            <div class="row items-center">
              <q-btn
                flat
                round
                dense
                icon="drag_indicator"
                class="drag-handle"
              />
              <q-btn
                flat
                round
                dense
                color="negative"
                icon="delete"
                class="delete-todo"
                @click="deleteTodoItem(todo)"
              />
            </div>
          </q-item-section>
        </q-item>
      </template>
    </draggable>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTodos } from '../composables/useTodos'
import draggable from 'vuedraggable'

const { todos, fetchTodos, addTodo, toggleTodo, deleteTodo, reorderTodos } = useTodos()

const newTodo = ref('')
const sortableTodos = computed({
  get: () => todos.value,
  set: (value) => {
    todos.value = value
  }
})

// Fetch todos when component is mounted
fetchTodos()

const addNewTodo = async () => {
  if (newTodo.value.trim()) {
    await addTodo(newTodo.value.trim())
    newTodo.value = ''
  }
}

const toggleTodoComplete = async (todo) => {
  await toggleTodo(todo)
}

const deleteTodoItem = async (todo) => {
  await deleteTodo(todo)
}

const onDragEnd = async ({ oldIndex, newIndex }) => {
  if (oldIndex === newIndex) return

  const newOrder = todos.value.map((todo, index) => ({
    id: todo.id,
    order: index + 1
  }))

  await reorderTodos(newOrder)
}
</script>

<style scoped>
.todo-list {
  max-width: 600px;
  margin: 0 auto;
}

.todo-item {
  transition: all 0.3s ease;
}

.todo-item.done {
  opacity: 0.7;
}

.drag-handle {
  cursor: move;
}
</style>
