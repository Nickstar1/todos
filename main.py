
from datetime import datetime
import uuid
from app.apis.open_street_map import get_latitude_longitude_address
from app.domain.location import Location
from app.domain.todo import Todo
from app.repositories.sql_lite_todo_repository import SQLiteTodoRepository
from app.services.create_todo_service import CreateTodoService
from app.services.location_resolver_service import LocationResolverService

import tkinter as tk

from app.services.read_all_todos_service import ReadAllTodosService
from app.services.update_todo_service import UpdateTodoService
from app.ui.todo_app import TodoApp


def main():
    repo = SQLiteTodoRepository('todos.db')
    try:
        read_all_todos_service: ReadAllTodosService = ReadAllTodosService(repo)
        todos = read_all_todos_service.run()

        TodoApp(repo, LocationResolverService(get_latitude_longitude_address), CreateTodoService(repo), todos)
    finally:
        print('closing db connection...')
        repo.close_connection()

if __name__ == '__main__':
    main()