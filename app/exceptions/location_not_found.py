class LocationNotFoundError(Exception):
    def __init__(self, id: int):
        super().__init__(f'location with id {id} not found')