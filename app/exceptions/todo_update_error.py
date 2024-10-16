import uuid


class TodoUpdateError(Exception):
    def __init__(self, todo_id: uuid.UUID, e: Exception):
        super().__init__(f'error updating todo with id {todo_id}: {e}')