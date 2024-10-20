import unittest
from unittest.mock import Mock
import uuid

from app.exceptions.todo_deletion_error import TodoDeletionError
from app.repositories.todo_repository import TodoRepository
from app.services.delete_todo_service import DeleteTodoService


class TestDeleteTodoService(unittest.TestCase):
    def setUp(self):
        self.mock_repo: Mock = Mock(spec=TodoRepository)
        self.service: DeleteTodoService = DeleteTodoService(self.mock_repo)

    def test_delete_todo_success(self):
        todo_id = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')

        self.service.run(todo_id)

        self.mock_repo.delete_todo.assert_called_once_with(todo_id)

    
    def test_delete_todo_deletion_failed(self):
        todo_id = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
        self.mock_repo.delete_todo.side_effect = Exception('database error')

        with self.assertRaises(TodoDeletionError):
            self.service.run(todo_id)