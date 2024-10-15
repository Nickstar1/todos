from abc import ABC, abstractmethod
from typing import List
import uuid

from app.domain.location import Location
from app.domain.todo import Todo

class TodoRepository(ABC):
    @abstractmethod
    def create_todo(self, todo: Todo) -> None:
        pass

    @abstractmethod
    def update_todo(self, todo: Todo) -> None:
        pass

    @abstractmethod
    def update_todo_location(self, location: Location) -> None:
        pass

    @abstractmethod
    def get_todo(self, id: uuid.UUID) -> Todo:
        pass

    @abstractmethod
    def get_all_todos(self) -> List[Todo]:
        pass

    @abstractmethod
    def delete_todo(self, id: uuid.UUID) -> None:
        pass