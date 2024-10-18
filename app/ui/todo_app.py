from datetime import datetime
import tkinter as tk
from tkinter import Button, Frame, messagebox
from typing import List, Optional

from app.apis.open_street_map import get_latitude_longitude_address
from app.domain.location import Location
from app.domain.todo import Todo
from app.repositories.todo_repository import TodoRepository
from app.services.complete_todo_service import CompleteTodoService
from app.services.create_todo_service import CreateTodoService
from app.services.delete_todo_service import DeleteTodoService
from app.services.location_resolver_service import LocationResolverService
from app.services.update_todo_service import UpdateTodoService
from app.ui.todo_dialog import todo_dialog
from app.ui.todo_item_component import TodoItemComponent

class TodoApp:
    def __init__(self, 
                 todo_repo: TodoRepository, 
                 location_resolver_service: LocationResolverService,
                 create_todo_service: CreateTodoService, 
                 todos: List[Todo]):
        # setup tkinter
        self.root = tk.Tk()
        self.root.title('TODO App')

        # init variables
        self.todo_repo: TodoRepository = todo_repo
        self.location_resolver_service: LocationResolverService = location_resolver_service
        self.create_todo_service: CreateTodoService = create_todo_service
        self.todos = todos
        self.todo_components: List[TodoItemComponent] = []
        self.add_todo_button: Optional[Frame] = None
        
        # initial render of ui
        self.render_todo_items()
        self.render_add_todo_button()

        # start main loop
        self.root.mainloop()

    def render_single_todo_item(self, todo: Todo):
        todo_component = TodoItemComponent(self.root, 
                                               todo, 
                                               CompleteTodoService(self.todo_repo),
                                               LocationResolverService(get_latitude_longitude_address), 
                                               UpdateTodoService(self.todo_repo), 
                                               DeleteTodoService(self.todo_repo))
        todo_component.pack(anchor='w', pady=5)
        self.todo_components.append(todo_component)

    def render_todo_items(self):
        for c in self.todo_components:
            c.destroy()
        self.todo_components.clear()

        for todo in self.todos:
            self.render_single_todo_item(todo)

    def render_add_todo_button(self):
        if self.add_todo_button:
            self.add_todo_button.destroy()

        self.add_todo_button = Frame(self.root)
        self.add_todo_button.pack(pady=10)

        new_todo_button = Button(self.add_todo_button, text="Add New Todo", command=self.open_new_todo_dialog)
        new_todo_button.pack()
        
    def open_new_todo_dialog(self):
        todo_dialog(self.root, 'New Todo', self.location_resolver_service.run, self.create_todo, 'Failed to add new todo', None)

    def create_todo(self, _: str, new_task: str, due_date: Optional[datetime], location: Optional[Location]):
        try:
            todo: Todo = self.create_todo_service.run(new_task, due_date, location)
            self.todos.append(todo)
            self.render_todo_items()  
            self.render_add_todo_button()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to add new todo: {e}')
