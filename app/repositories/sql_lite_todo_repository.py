import sqlite3
from sqlite3 import Connection, Cursor
from typing import List
import uuid

from app.domain.location import Location
from app.domain.todo import Todo
from app.exceptions.todo_not_found import TodoNotFoundError
from app.repositories.todo_repository import TodoRepository


class SQLiteTodoRepository(TodoRepository):
    def __init__(self, db_file: str):
        self.connection: Connection = self.create_connection(db_file)
        self.create_tables()

    def create_connection(self, db_file: str) -> Connection:
        connection: Connection = None
        try:
            connection = sqlite3.connect(db_file)
            print(f'conntected to {db_file}')
        except Exception as e:
            print(f'could not connect to db: {e}')

        return connection

    def close_connection(self):
        if not self.connection:
            print('tried closing connection to db but connection was None')
            return
        self.connection.close()

    def create_tables(self):
        create_location_table = '''
        CREATE TABLE IF NOT EXISTS location (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            address TEXT NOT NULL
        );
        '''

        create_todo_table = '''
        CREATE TABLE IF NOT EXISTS todo (
            id TEXT PRIMARY KEY,
            task TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            completed BOOLEAN DEFAULT 0,
            location_id INTEGER,  -- Foreign key to location
            due_date DATETIME,
            updated_at DATETIME,
            FOREIGN KEY (location_id) REFERENCES location (id) ON DELETE SET NULL
        );
        '''

        try:
            cursor: Cursor = self.connection.cursor()
            cursor.execute(create_location_table)
            cursor.execute(create_todo_table)
            print('initial tables created successfully')
        except Exception as e:
            print(f'error creating tables: {e}')
        finally:
            cursor.close()

    def create_todo(self, todo: Todo) -> None:
        cursor: Cursor = self.connection.cursor()
        location_id: int = None
        if todo.location is not None:
            insert_location_query = '''
            INSERT INTO location (latitude, longitude, address)
            VALUES (?, ?, ?);
            '''

            try:
                cursor.execute(insert_location_query, (todo.location.latitude, todo.location.longitude, todo.location.address))
                location_id = cursor.lastrowid
            except Exception as e:
                print(f'error inserting location: {e}')
                cursor.close()
                return None

        try:
            insert_todo_query = '''
            INSERT INTO todo (id, task, completed, location_id, due_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            '''

            cursor.execute(insert_todo_query, (
                str(todo.id),
                todo.task,
                todo.completed,
                location_id,
                todo.due_date,
                todo.created_at,
                todo.updated_at
            ))

            self.connection.commit()
        except Exception as e:
            print(f'error creating todo: {e}')
            self.connection.rollback()
        finally:
            cursor.close()


    def update_todo(self, todo: Todo) -> None:
        cursor: Cursor = self.connection.cursor()

        update_todo_query = '''
        UPDATE todo
        SET task = ?, completed = ?, due_date = ?, updated_at = ?
        WHERE id = ?;
        '''

        try: 
            cursor.execute(update_todo_query, (
                todo.task,
                todo.completed,
                todo.due_date,
                todo.updated_at,
                str(todo.id)
            ))
            self.connection.commit()
        except Exception as e:
            print(f'error updating todo: {e}')
            self.connection.rollback()
        finally:
            cursor.close()

    def update_todo_location(self, location: Location) -> None:
        cursor: Cursor = self.connection.cursor()

        update_location_query = '''
        UPDATE location
        SET latitude = ?, longitude = ?, address = ?, updated_at = ?
        WHERE id = ?;
        '''

        #
        # TODO: update updated_at in todo
        #

        try: 
            cursor.execute(update_location_query, (
                location.latitude,
                location.longitude,
                location.address,
                location.id,
            ))
            self.connection.commit()
        except Exception as e:
            print(f'error updating location: {e}')
            self.connection.rollback()
        finally:
            cursor.close()

    def get_todo(self, id: uuid.UUID) -> Todo:
        cursor: Cursor = self.connection.cursor()

        query = '''
        SELECT t.id, t.task, t.completed, t.location_id, t.due_date, t.created_at, t.updated_at, 
           l.latitude, l.longitude, l.address
        FROM todo t
        LEFT JOIN location l ON t.location_id = l.id
        WHERE t.id = ?;
        '''

        try:
            cursor.execute(query, (str(id),))
            row = cursor.fetchone()

            if row is None:
                raise TodoNotFoundError(id)
            
            location: Location = Location(
                id=row[3],
                latitude=row[7],
                longitude=row[8],
                address=row[9]
            ) if row[3] is not None else None

            return Todo(
                id=uuid.UUID(row[0]),
                task=row[1],
                completed=row[2],
                location_id=location.id if location is not None else None,
                location=location,
                due_date=row[4],
                created_at=row[5],
                updated_at=row[6]
            )
        except Exception as e:
            print(f'error reading todo: {e}')
            raise
        finally:
            cursor.close()


    def get_all_todos(self) -> List[Todo]:
        cursor: Cursor = self.connection.cursor()

        query = '''
        SELECT t.id, t.task, t.completed, t.location_id, t.due_date, t.created_at, t.updated_at, 
           l.latitude, l.longitude, l.address
        FROM todo t
        LEFT JOIN location l ON t.location_id = l.id;
        '''

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            todos: List[Todo] = []
            for row in rows:
                location: Location = Location(
                    id=row[3],
                    latitude=row[7],
                    longitude=row[8],
                    address=row[9]
                ) if row[3] is not None else None

                todo: Todo = Todo(
                    id=uuid.UUID(row[0]),
                    task=row[1],
                    completed=row[2],
                    location_id=location.id if location is not None else None,
                    location=location,
                    due_date=row[4],
                    created_at=row[5],
                    updated_at=row[6]
                )
                todos.append(todo)

            return todos
        except Exception as e:
            print(f'error reading todos: {e}')
            raise
        finally:
            cursor.close()
                

    def delete_todo(self, id: uuid.UUID) -> None:
        cursor: Cursor = self.connection.cursor()

        select_query = '''
        SELECT * FROM todo WHERE id = ?;
        '''

        try:
            cursor.execute(select_query, (str(id),))
            row = cursor.fetchone()

            if row is None:
                raise TodoNotFoundError(id)
            
            delete_query = '''
            DELETE FROM todo WHERE id = ?;
            '''
            cursor.execute(delete_query, (str(id),))
            self.connection.commit()
        except Exception as e:
            print(f'error deleting todo: {e}')
            self.connection.rollback()
            raise
        finally:
            cursor.close()