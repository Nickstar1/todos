from typing import List
from app.domain.todo import Todo
from app.exceptions.read_all_todos_error import ReadAllTodosError
from app.repositories.todo_repository import TodoRepository


class ReadAllTodosService:
    def __init__(self, todo_repo: TodoRepository):
        self.todo_repo: TodoRepository = todo_repo

    def run(self) -> List[Todo]:
        try:
            return self.todo_repo.get_all_todos()
        except Exception as e:
            print(f'todo could not be retrieved: {e}')
            raise ReadAllTodosError(e)