<template>
  <div class="container">
    <h1 class="my-4">To-Do List</h1>
    
    <form @submit.prevent="addTodo" class="input-group mb-3">
      <input type="text" class="form-control" v-model="newTask" placeholder="New task">
      <button class="btn btn-primary" type="submit">Add</button>
    </form>
    
    <ul class="list-group">
      <li v-for="todo in todos" :key="todo.id" class="list-group-item d-flex justify-content-between align-items-center">
        <input type="text" class="form-control" v-model="todo.task" @blur="updateTodo(todo)">
        <button class="btn btn-danger btn-sm" @click="deleteTodo(todo.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001';

export default {
  name: 'App',
  data() {
    return {
      todos: [],
      newTask: ''
    };
  },
  created() {
    this.fetchTodos();
  },
  methods: {
    async fetchTodos() {
      try {
        const response = await axios.get(`${API_BASE_URL}/todos`);
        this.todos = response.data;
      } catch (error) {
        console.error('Error fetching todos:', error);
      }
    },
    async addTodo() {
      if (this.newTask.trim() === '') return;

      try {
        const response = await axios.post(`${API_BASE_URL}/todos`, {
          task: this.newTask
        });
        this.todos.push(response.data);
        this.newTask = '';
      } catch (error) {
        console.error('Error adding todo:', error);
      }
    },
    async updateTodo(todo) {
      try {
        await axios.put(`${API_BASE_URL}/todos/${todo.id}`, {
          task: todo.task
        });
      } catch (error) {
        console.error('Error updating todo:', error);
      }
    },
    async deleteTodo(id) {
      try {
        await axios.delete(`${API_BASE_URL}/todos/${id}`);
        this.todos = this.todos.filter(todo => todo.id !== id);
      } catch (error) {
        console.error('Error deleting todo:', error);
      }
    }
  }
};
</script>

<style>
.container {
  max-width: 600px;
  margin-top: 50px;
}
</style>
