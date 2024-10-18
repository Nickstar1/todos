
from datetime import datetime
from tkinter import Button, Entry, Label, Toplevel, messagebox
from typing import Callable, Optional

from app.domain.location import Location
from app.domain.todo import Todo

ResolveLocationType = Callable[[str], Location]

DUE_DATE_PLACEHOLDER: str = 'YYYY-MM-DD'

def todo_dialog(root, title: str, resolve_location: ResolveLocationType, save_todo: Callable, error_msg: str, todo: Optional[Todo] = None) -> Toplevel:
    popup = Toplevel(root)
    popup.title(title)

    # Task input
    Label(popup, text="Task:").grid(row=0, column=0)
    task_entry = Entry(popup)
    task_entry.grid(row=0, column=1)
    task_entry.insert(0, todo.task if todo else '')

    # Due Date input
    Label(popup, text="Due Date:").grid(row=1, column=0)
    due_date_entry = Entry(popup)
    due_date_entry.grid(row=1, column=1)
    due_date_entry.insert(0, todo.due_date.strftime('%Y-%m-%d') if todo and todo.due_date else DUE_DATE_PLACEHOLDER)  

    # Location input
    Label(popup, text="Address:").grid(row=2, column=0)
    location_entry = Entry(popup)
    location_entry.grid(row=2, column=1)
    location_entry.insert(0, todo.location.address if todo and todo.location else '')

    def apply_changes():
        new_task = task_entry.get()
        if not new_task.strip():
            messagebox.showerror('Error', 'A task description cannot be empty')
            return
        
        due_date_entry_str = due_date_entry.get()
        due_date: Optional[datetime] = None
        if due_date_entry_str.strip() and due_date_entry_str.strip() != DUE_DATE_PLACEHOLDER:
            try:
                due_date = datetime.strptime(due_date_entry_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror('Error', 'Please enter the date in YYYY-MM-DD format.')
                return

        location_entry_str = location_entry.get()
        location: Optional[Location] = None
        if location_entry_str.strip():
            try:
                location = resolve_location(location_entry_str.strip())
            except Exception:
                messagebox.showerror('Error', 'Addess not found.')
                return
        
        try:
            save_todo(todo.id if todo else '', new_task, due_date, location)
            popup.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'{error_msg}: {e}')


    Button(popup, text="Save", command=apply_changes).grid(row=3, column=1)

