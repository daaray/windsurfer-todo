import { ref } from 'vue'
import axios from 'axios'
import { Notify } from 'quasar'

export function useTodos() {
  const todos = ref([])

  const fetchTodos = async () => {
    try {
      const response = await axios.get('/api/todos/')
      todos.value = response.data
    } catch (error) {
      console.error('Error fetching todos:', error)
      Notify.create({
        type: 'negative',
        message: 'Failed to fetch todos'
      })
    }
  }

  const addTodo = async (title) => {
    try {
      const response = await axios.post('/api/todos/', {
        title,
        completed: false
      })
      todos.value.push(response.data)
      Notify.create({
        type: 'positive',
        message: 'Todo added successfully'
      })
    } catch (error) {
      console.error('Error adding todo:', error)
      Notify.create({
        type: 'negative',
        message: 'Failed to add todo'
      })
    }
  }

  const toggleTodo = async (todo) => {
    try {
      const response = await axios.patch(`/api/todos/${todo.id}/`, {
        completed: !todo.completed
      })
      const index = todos.value.findIndex(t => t.id === todo.id)
      if (index !== -1) {
        todos.value[index] = response.data
      }
    } catch (error) {
      console.error('Error toggling todo:', error)
      Notify.create({
        type: 'negative',
        message: 'Failed to update todo'
      })
    }
  }

  const deleteTodo = async (todo) => {
    try {
      await axios.delete(`/api/todos/${todo.id}/`)
      todos.value = todos.value.filter(t => t.id !== todo.id)
      Notify.create({
        type: 'positive',
        message: 'Todo deleted successfully'
      })
    } catch (error) {
      console.error('Error deleting todo:', error)
      Notify.create({
        type: 'negative',
        message: 'Failed to delete todo'
      })
    }
  }

  const reorderTodos = async (newOrder) => {
    try {
      await axios.post('/api/todos/reorder/', newOrder)
      await fetchTodos() // Refresh the list after reordering
      Notify.create({
        type: 'positive',
        message: 'Todos reordered successfully'
      })
    } catch (error) {
      console.error('Error reordering todos:', error)
      Notify.create({
        type: 'negative',
        message: 'Failed to reorder todos'
      })
    }
  }

  return {
    todos,
    fetchTodos,
    addTodo,
    toggleTodo,
    deleteTodo,
    reorderTodos
  }
}
