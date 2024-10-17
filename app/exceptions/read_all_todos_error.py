class ReadAllTodosError(Exception):
    def __init__(self, e: Exception):
        super().__init__(f'error reading todos: {e}')