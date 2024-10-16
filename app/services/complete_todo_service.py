from datetime import datetime
from typing import Optional
import uuid
from app.domain.todo import Todo
from app.exceptions.todo_completion_error import TodoCompletionError
from app.repositories.todo_repository import TodoRepository


class CompleteTodoService:
    def __init__(self, todo_repo: TodoRepository):
        self.todo_repo: TodoRepository = todo_repo

    def run(self, todo_id: uuid.UUID) -> Todo:
        todo: Optional[Todo] = None

        try:
            todo = self.todo_repo.get_todo(todo_id)
        except Exception as e:
            print(f'failed to retrieve todo with id {todo_id}: {e}')
            raise TodoCompletionError(todo_id, e)

        todo.completed = True
        todo.updated_at = datetime.now()

        try: 
            self.todo_repo.update_todo(todo)
        except Exception as e:
            print(f'failed to mark todo {todo_id} as completed: {e}')
            raise TodoCompletionError(todo_id, e)

        return todo
