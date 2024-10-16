class TodoCreationError(Exception):
    def __init__(self, task: str, e: Exception):
          super().__init__(f'error creating todo {task}: {e}')