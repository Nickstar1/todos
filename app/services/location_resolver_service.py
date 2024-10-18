from app.domain.location import Location
from app.exceptions.location_fetch_error import LocationFetchError
from app.exceptions.no_location_found_error import NoLocationFoundError


class LocationResolverService:
    def __init__(self, get_latitude_longitude_address):
        self.get_latitude_longitude_address = get_latitude_longitude_address

    def run(self, address: str) -> Location:
        try:
            latitude, longitude, address = self.get_latitude_longitude_address(address)
            return Location(address=address, latitude=latitude, longitude=longitude)
        except (LocationFetchError, NoLocationFoundError) as e:
            print(f'error resolving location for address: {e}')
            raise