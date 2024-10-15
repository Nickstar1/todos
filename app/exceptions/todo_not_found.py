import uuid


class TodoNotFoundError(Exception):
    def __init__(self, id: uuid.UUID):
        super().__init__(f'todo with id {id} not found')