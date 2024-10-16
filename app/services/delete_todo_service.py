import uuid
from app.exceptions.todo_deletion_error import TodoDeletionError
from app.repositories.todo_repository import TodoRepository


class DeleteTodoService:
    def __init__(self, todo_repo: TodoRepository):
        self.todo_repo: TodoRepository = todo_repo

    def run(self, todo_id: uuid.UUID) -> None:
        try: 
            self.todo_repo.delete_todo(todo_id)
        except Exception as e:
            print(f'failed to delete todo with id {todo_id}: {e}')
            raise TodoDeletionError(todo_id, e)