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


    def __eq__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        return (self.address, self.latitude, self.longitude) == (other.address, other.latitude, other.longitude)