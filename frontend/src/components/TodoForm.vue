<template>
  <form @submit.prevent="handleSubmit">
    <q-input
      v-model="newTodo"
      label="Add a new todo"
      dense
      outlined
      class="q-mb-md"
      @keyup.enter="handleSubmit"
    >
      <template v-slot:append>
        <q-btn
          round
          dense
          flat
          icon="add"
          type="submit"
          :disable="!newTodo.trim()"
        />
      </template>
    </q-input>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const newTodo = ref('')
const emit = defineEmits(['add-todo'])

const handleSubmit = () => {
  const todoText = newTodo.value.trim()
  if (todoText) {
    emit('add-todo', todoText)
    newTodo.value = ''
  }
}
</script>
