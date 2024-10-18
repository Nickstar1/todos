from datetime import datetime
from typing import Optional
import uuid
from app.domain.location import Location
from app.domain.todo import Todo
from app.exceptions.todo_update_error import TodoUpdateError
from app.repositories.todo_repository import TodoRepository


class UpdateTodoService:
    def __init__(self, todo_repo: TodoRepository):
        self.todo_repo: TodoRepository = todo_repo

    def run(self, todo_id: uuid.UUID, task: str, location: Optional[Location], due_date: Optional[datetime]) -> Todo:
        if not task.strip():
            raise ValueError('task cannot be empty')
        
        if due_date and due_date.date() < datetime.now().date():
            raise ValueError('due date cannot be in the past')
        
        todo: Optional[Todo] = None

        try:
            todo = self.todo_repo.get_todo(todo_id)
        except Exception as e:
            print(f'failed to retrieve todo with id {todo_id}: {e}')
            raise TodoUpdateError(todo_id, e)
        
        if todo.task == task and todo.location == location and todo.due_date == due_date:
            return todo
        
        if todo.location is None and location is not None:
            # create location
            try: 
                location_id: int = self.todo_repo.create_todo_location(location)
                todo.location_id = location_id
            except Exception as e:
                print(f'failed to create todo location for todo {todo_id}: {e}')
                raise TodoUpdateError(todo_id, e)

        if todo.location is not None and todo.location != location and location is not None:
            # update location 
            try:
                todo.location.latitude = location.latitude
                todo.location.longitude = location.longitude
                todo.location.address = location.address
                self.todo_repo.update_todo_location(todo.location)
            except Exception as e:
                print(f'failed to update todo location for todo {todo_id}: {e}')
                raise TodoUpdateError(todo_id, e)

        if todo.location is not None and location is None:
            # delete location & location_id
            try:
                self.todo_repo.delete_todo_location(todo.location_id)
                todo.location_id = None
            except Exception as e:
                print(f'failed to delete todo location for todo {todo_id}: {e}')
                raise TodoUpdateError(todo_id, e)
        

        todo.task = task
        todo.due_date = due_date
        todo.updated_at = datetime.now()

        try: 
            self.todo_repo.update_todo(todo)
        except Exception as e:
            print(f'failed to update todo with id {todo_id}: {e}')
            raise TodoUpdateError(todo_id, e)
        
        try:
            return self.todo_repo.get_todo(todo_id)
        except Exception as e:
            print(f'failed to retrieve updated todo with id {todo_id}: {e}')
            raise TodoUpdateError(todo_id, e)