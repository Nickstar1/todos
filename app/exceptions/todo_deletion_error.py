import uuid


class TodoDeletionError(Exception):
    def __init__(self, todo_id: uuid.UUID, e: Exception):
        super().__init__(f'error deleting todo with id {todo_id}: {e}')