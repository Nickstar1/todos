class NoLocationFoundError(Exception):
    def __init__(self, address: str):
        super().__init__(f'no location found for address: {address}')