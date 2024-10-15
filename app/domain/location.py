from typing import Optional


class Location:
    def __init__(self, 
                 latitude: float, 
                 longitude: float, 
                 address: str,
                 id: Optional[int] = None):
        self.id: Optional[int] = id
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.address: str = address