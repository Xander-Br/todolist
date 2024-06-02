<template>
  <div id="app" class="container d-flex flex-column align-items-center justify-content-center vh-100">
    <div class="card w-75 w-md-50 w-lg-25 mb-4">
      <div class="card-body">
        <h2 class="card-title text-center">Create todo</h2>
        <textarea
          v-model="newTask"
          class="form-control mb-3"
          rows="3"
          placeholder="Enter your task here"
        ></textarea>
        <button class="btn btn-primary w-100" @click="addTodo">Submit</button>
      </div>
    </div>
    <div class="w-75 w-md-50 w-lg-25">
      <ul class="list-group">
        <li
          v-for="todo in todos"
          :key="todo.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          <input
            v-model="todo.task"
            @change="updateTodo(todo)"
            type="text"
            class="form-control me-2"
          />
          <button class="btn btn-danger" @click="deleteTodo(todo.id)">
            Delete
          </button>
        </li>
      </ul>
    </div>
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
#app {
  margin-top: 60px;
}
.card {
  margin-bottom: 20px;
}
.list-group-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.form-control {
  flex: 1;
}
.btn-danger {
  margin-left: 10px;
}
</style>
