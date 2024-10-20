from datetime import datetime
from typing import List
import unittest
from unittest.mock import Mock
import uuid

from app.domain.todo import Todo
from app.exceptions.read_all_todos_error import ReadAllTodosError
from app.repositories.todo_repository import TodoRepository
from app.services.read_all_todos_service import ReadAllTodosService


class TestReadAllTodosService(unittest.TestCase):
    def setUp(self):
        self.mock_repo: Mock = Mock(spec=TodoRepository)
        self.service: ReadAllTodosService = ReadAllTodosService(self.mock_repo)

    
    def test_read_all_todos_success(self):
        todos: List[Todo] = [
            Todo(
                id=uuid.UUID('123e4567-e89b-12d3-a456-426614174000'),
                task='Do the dishes',
                completed=True,
                created_at=datetime(2024, 10, 4)
            ),
            Todo(
                id=uuid.UUID('123e4567-e89b-12d3-a456-426614174001'),
                task='Take out trash',
                completed=False,
                created_at=datetime(2024, 10, 5)
            ),
        ]

        self.mock_repo.get_all_todos.return_value = todos

        result = self.service.run()

        self.mock_repo.get_all_todos.assert_called_once()
        self.assertEqual(result, todos)


    def test_read_all_todos_retrieval_failed(self):
        self.mock_repo.get_all_todos.side_effect = Exception('database error')

        with self.assertRaises(ReadAllTodosError):
            self.service.run()

        self.mock_repo.get_all_todos.called_once()