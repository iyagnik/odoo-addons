/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.uqID = 1;
  }

  addTodoItem(ev) {
    if (ev.keyCode === 13 && ev.target.value != "") {
      this.todos.push({
        id: this.uqID++,
        description: ev.target.value,
        isDone: false,
      });
      ev.target.value = "";
    }
  }

  toggleTodo(todoId) {
    const todo = this.todos.find((todo) => todo.id === todoId);
    if (todo) {
      todo.isDone = !todo.isDone;
    }
  }

  removeTodo(todoId) {
    const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
    if (todoIndex >= 0) {
        this.todos.splice(todoIndex, 1);
    }
}
}
