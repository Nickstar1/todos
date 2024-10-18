from datetime import datetime
import tkinter as tk
from tkinter import Canvas, Frame, Label, Menu, ttk
from tkinter import messagebox
from typing import Optional

from app.domain.location import Location
from app.domain.todo import Todo
from app.services.complete_todo_service import CompleteTodoService
from app.services.delete_todo_service import DeleteTodoService
from app.services.location_resolver_service import LocationResolverService
from app.services.update_todo_service import UpdateTodoService
from app.ui.todo_dialog import todo_dialog

class TodoItemComponent(ttk.Frame):
    def __init__(self, 
                 master: tk.Tk, 
                 todo: Todo, 
                 complete_todo_service: CompleteTodoService, 
                 location_resolver_service: LocationResolverService,
                 update_todo_service: UpdateTodoService, 
                 delete_todo_service: DeleteTodoService):
        super().__init__(master)

        self.todo: Todo = todo
        self.complete_todo_service: CompleteTodoService = complete_todo_service
        self.location_resolver_service: LocationResolverService = location_resolver_service
        self.update_todo_service: UpdateTodoService = update_todo_service
        self.delete_todo_service: DeleteTodoService = delete_todo_service

        # circular button
        self.circle_canvas = Canvas(self, width=30, height=30, highlightthickness=0)
        self.draw_circle(self.todo.completed)
        self.circle_canvas.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
        self.circle_canvas.bind('<Button-1>', self.complete_task)

        # row1 frame for alignment and click event
        self.row1_frame = Frame(self)
        self.row1_frame.grid(row=0, column=1, sticky='w')
        self.row1_frame.bind('<Button-1>', self.show_menu)
        # row2 frame for alignment and click event
        self.row2_frame = Frame(self)
        self.row2_frame.grid(row=1, column=1, sticky='w')
        self.row2_frame.bind('<Button-1>', self.show_menu)

        # task label
        self.task_label = Label(self.row1_frame, text=todo.task, font=('Arial', 12, "bold"))
        self.task_label.grid(row=0, column=1, sticky='w')
        self.task_label.bind('<Button-1>', self.show_menu)

        # due date
        due_date_text: str = ''
        if self.todo.due_date:
            due_date_text = self.todo.due_date.strftime('%Y-%m-%d')
        self.due_date_label = Label(self.row1_frame, text=due_date_text, font=("Arial", 10, "italic"), fg="red")
        self.due_date_label.grid(row=0, column=2, sticky="w", padx=(5,10))
        self.due_date_label.bind('<Button-1>', self.show_menu)

        # location
        address: str = ''
        lat_lon: str = ''
        if self.todo.location:
            address = self.todo.location.address 
            lat_lon = f'{self.todo.location.latitude, self.todo.location.longitude}' 
        self.location_label = Label(self.row2_frame, text=f'{address} {lat_lon}', font=('Arial', 10, 'italic'))
        self.location_label.grid(row=1, column=1, sticky='w', padx=(0, 10))
        self.location_label.bind('<Button-1>', self.show_menu)

        # menu
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label='Edit', command=self.edit_todo)
        self.menu.add_command(label='Delete', command=self.delete_todo)

    def draw_circle(self, completed):
        self.circle_canvas.delete("all")
        if completed:
            self.circle_canvas.create_oval(5, 5, 25, 25, outline="black", fill="gray")
            self.circle_canvas.create_line(5, 5, 25, 25, fill="white", width=2)
            self.circle_canvas.create_line(5, 25, 25, 5, fill="white", width=2)
        else:
            self.circle_canvas.create_oval(5, 5, 25, 25, outline="black", fill="white")

    def complete_task(self, event):
        try:
            self.todo = self.complete_todo_service.run(self.todo.id)
            self.draw_circle(self.todo.completed)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to complete the task: {e}')

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def edit_todo(self):
        todo_dialog(self, 'Edit Todo', self.location_resolver_service.run, self.update_todo, 'Failed to update the task', self.todo)

    def update_todo(self, id: str, new_task: str, due_date: Optional[datetime], location: Optional[Location]):
        self.todo = self.update_todo_service.run(self.todo.id, new_task, location, due_date)
        self.refresh_ui()


    def delete_todo(self):
        answer = messagebox.askyesno('Delete', f'Do you really want to delete the task: {self.todo.task}')
        if answer:
            try: 
                self.delete_todo_service.run(self.todo.id)
                self.destroy()
            except Exception as e:
                messagebox.showerror('Error', f'Failed to delete the task: {e}')



    def refresh_ui(self):
        self.task_label.config(text=self.todo.task)

        due_date_text = self.todo.due_date.strftime('%Y-%m-%d') if self.todo.due_date else ''
        self.due_date_label.config(text=due_date_text)

        address: str = ''
        lat_lon: str = ''
        if self.todo.location:
            address = self.todo.location.address 
            lat_lon = f'{self.todo.location.latitude, self.todo.location.longitude}' 
        self.location_label.config(text=f'{address} {lat_lon}')
