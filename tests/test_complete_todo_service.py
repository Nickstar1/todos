from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import uuid

from app.domain.todo import Todo
from app.exceptions.todo_completion_error import TodoCompletionError
from app.repositories.todo_repository import TodoRepository
from app.services.complete_todo_service import CompleteTodoService


class TestCompleteTodoService(unittest.TestCase):
    def setUp(self):
        self.mock_repo: Mock = Mock(spec=TodoRepository)
        self.service: CompleteTodoService = CompleteTodoService(self.mock_repo)

    @patch('app.services.complete_todo_service.datetime')
    def test_complete_todo_success(self, mock_datetime):
        todo_id = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
        updated_at = datetime(2024, 9, 2)

        mock_datetime.now.return_value = updated_at
        
        todo = Todo(
            id=todo_id, 
            task='Do the dishes',
            created_at=datetime(2024, 9, 1)
        )

        self.mock_repo.get_todo.return_value = todo
        self.mock_repo.update_todo.return_value = None

        result = self.service.run(todo_id)

        self.mock_repo.get_todo.assert_called_once_with(todo_id)
        self.mock_repo.update_todo.assert_called_once()
        self.assertTrue(result.completed)
        self.assertEqual(result.updated_at, updated_at)


def test_complete_todo_retrieval_failed(self):
    self.mock_repo.get_todo.side_effect = Exception('database error')

    with self.assertRaises(TodoCompletionError):
        self.service.run(uuid.UUID('123e4567-e89b-12d3-a456-426614174000'))


def test_complete_todo_update_failed(self):
    todo_id = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
    todo = Todo(
        id=todo_id, 
        task='Do the dishes',
        created_at=datetime(2024, 9, 1)
    )

    self.mock_repo.get_todo.return_value = todo
    self.mock_repo.update_todo.side_effect = Exception('database error')

    with self.assertRaises(TodoCompletionError):
        self.service.run(todo_id)