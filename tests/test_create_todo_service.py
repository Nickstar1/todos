from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import uuid

from app.domain.todo import Todo
from app.exceptions.todo_creation_error import TodoCreationError
from app.repositories.todo_repository import TodoRepository
from app.services.create_todo_service import CreateTodoService


class TestCreateTodoService(unittest.TestCase):
    def setUp(self):
        self.mock_repo: Mock = Mock(spec=TodoRepository)
        self.service: CreateTodoService = CreateTodoService(self.mock_repo)

    @patch('app.services.create_todo_service.uuid.uuid4')
    @patch('app.services.create_todo_service.datetime')
    def test_create_todo_success(self, mock_datetime, mock_uuid):
        todo_id = uuid.uuid4()
        created_at = datetime(2024, 9, 1)

        mock_uuid.return_value = todo_id
        mock_datetime.now.return_value = created_at
        
        task = 'Do the dishes'

        todo = Todo(
            id=todo_id,
            task=task,
            created_at=created_at
        )

        self.mock_repo.create_todo.return_value = None
        self.mock_repo.get_todo.return_value = todo

        result = self.service.run(task=task)

        self.mock_repo.create_todo.assert_called_once()
        self.mock_repo.get_todo.assert_called_once_with(todo_id)
        self.assertEqual(result.task, task)
        self.assertEqual(result.completed, False)


    def test_create_todo_empty_task(self):
        task = ''
        with self.assertRaises(ValueError):
            self.service.run(task)


    @patch('app.services.create_todo_service.datetime')
    def test_create_todo_due_date_in_the_past(self, mock_datetime):
        task = 'Do the dishes'
        due_date = datetime(2024, 8, 1)

        mock_datetime.now.return_value = datetime(2024, 9, 1)

        with self.assertRaises(ValueError):
            self.service.run(task, due_date)

    
    def test_create_todo_creation_failed(self):
        task = 'Do the dishes'
        self.mock_repo.create_todo.side_effect = Exception('database error')

        with self.assertRaises(TodoCreationError):
            self.service.run(task)

        self.mock_repo.create_todo.assert_called_once()


    def test_create_todo_retrieval_failed(self):
        task = 'Do the dishes'
        self.mock_repo.create_todo.return_value = None
        self.mock_repo.get_todo.side_effect = Exception('database error')

        with self.assertRaises(TodoCreationError):
            self.service.run(task)

        self.mock_repo.create_todo.assert_called_once()
        self.mock_repo.get_todo.assert_called_once()
