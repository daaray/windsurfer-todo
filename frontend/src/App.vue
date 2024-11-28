<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>
          Todo List
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page padding>
        <!-- Add Todo Form -->
        <div class="q-mb-lg">
          <div class="row q-gutter-sm">
            <q-input
              v-model="newTodo"
              filled
              class="col text-dark"
              name="todo-input"
              id="todo-input"
              label="Add a new todo"
              placeholder="Add a new todo..."
              @keyup.enter="addTodo"
            />
            <q-btn
              color="primary"
              label="Add Todo"
              @click="addTodo"
              :disable="!newTodo.trim()"
              flat
              class="q-px-md"
            >
              <template v-slot:default>
                <span class="text-white">Add Todo</span>
                <q-icon name="add" color="white" class="q-ml-sm" />
              </template>
            </q-btn>
          </div>
        </div>

        <!-- Todo List -->
        <q-list bordered separator>
          <draggable
            v-model="todos"
            @end="onDragEnd"
            item-key="id"
            handle=".drag-handle"
          >
            <template #item="{ element: todo }">
              <q-item>
                <q-item-section avatar class="drag-handle cursor-move">
                  <q-icon name="drag_indicator" />
                </q-item-section>

                <q-item-section avatar>
                  <q-checkbox
                    v-model="todo.completed"
                    @update:model-value="toggleTodo(todo)"
                  />
                </q-item-section>

                <q-item-section>
                  <q-item-label :class="{ 'text-strike': todo.completed }">
                    {{ todo.title }}
                  </q-item-label>
                </q-item-section>

                <q-item-section side>
                  <q-btn
                    flat
                    round
                    dense
                    color="negative"
                    @click="deleteTodo(todo.id)"
                  >
                    <template v-slot:default>
                      <q-icon name="delete" color="white" />
                    </template>
                  </q-btn>
                </q-item-section>
              </q-item>
            </template>
          </draggable>
        </q-list>

        <div v-if="todos.length === 0" class="text-center q-mt-lg text-dark">
          <q-icon name="check_circle" size="48px" color="positive" />
          <div class="text-h6 q-mt-sm">All done! Add a new todo to get started.</div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import draggable from 'vuedraggable'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// Configure notifications
const showNotification = (message, type = 'positive') => {
  $q.notify({
    message,
    color: type,
    textColor: 'white',
    icon: type === 'positive' ? 'check_circle' : 'warning',
    position: 'top-right',
    actions: [{ icon: 'close', color: 'white' }]
  })
}

const API_URL = 'http://localhost:8000/api/todos/'
const todos = ref([])
const newTodo = ref('')

// Fetch all todos
const fetchTodos = async () => {
  console.log('Fetching todos...')
  try {
    const response = await axios.get(API_URL)
    todos.value = response.data
  } catch (error) {
    console.error('Error fetching todos:', error)
    showNotification('Failed to load todos', 'negative')
  }
}

// Add a new todo
const addTodo = async () => {
  console.log('Add todo button clicked')
  if (!newTodo.value.trim()) {
    console.log('Empty todo, showing warning')
    showNotification('Please enter a todo item', 'warning')
    return
  }

  try {
    const response = await axios.post(API_URL, {
      title: newTodo.value.trim(),
      completed: false,
      order: todos.value.length
    })

    todos.value.unshift(response.data)
    newTodo.value = ''
    
    showNotification('Todo added successfully')
  } catch (error) {
    console.error('Error details:', error)
    showNotification(`Failed to add todo: ${error.response?.data?.detail || 'An error occurred while adding the todo'}`, 'negative')
  }
}

// Toggle todo completion
const toggleTodo = async (todo) => {
  try {
    const response = await axios.patch(`${API_URL}${todo.id}/`, {
      completed: todo.completed
    })
    const index = todos.value.findIndex(t => t.id === todo.id)
    todos.value[index] = response.data
    showNotification(todo.completed ? 'Todo completed!' : 'Todo uncompleted', todo.completed ? 'positive' : 'info')
  } catch (error) {
    console.error('Error updating todo:', error)
    showNotification(`Failed to update todo: ${error.response?.data?.detail || 'An error occurred while updating the todo'}`, 'negative')
  }
}

// Delete a todo
const deleteTodo = async (id) => {
  try {
    await axios.delete(`${API_URL}${id}/`)
    todos.value = todos.value.filter(todo => todo.id !== id)
    showNotification('Todo deleted')
  } catch (error) {
    console.error('Error deleting todo:', error)
    showNotification(`Failed to delete todo: ${error.response?.data?.detail || 'An error occurred while deleting the todo'}`, 'negative')
  }
}

// Handle drag end
const onDragEnd = async () => {
  try {
    const reorderedTodos = todos.value.map((todo, index) => ({
      id: todo.id,
      order: index
    }))
    
    await axios.post(`${API_URL}reorder/`, reorderedTodos)
    showNotification('Todos reordered successfully')
  } catch (error) {
    console.error('Error reordering todos:', error)
    showNotification('Failed to reorder todos', 'negative')
    // Refresh the list to get the correct order
    await fetchTodos()
  }
}

// Load todos when component mounts
onMounted(fetchTodos)
</script>

<style lang="scss">
.drag-handle {
  cursor: move;
  user-select: none;
}
</style>
