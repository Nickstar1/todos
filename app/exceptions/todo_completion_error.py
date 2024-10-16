import uuid


class TodoCompletionError(Exception):
    def __init__(self, todo_id: uuid.UUID, e: Exception):
        super().__init__(f'error completing todo with id {todo_id}: {e}')