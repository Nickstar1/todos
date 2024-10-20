import unittest
from unittest.mock import Mock

from app.domain.location import Location
from app.exceptions.location_fetch_error import LocationFetchError
from app.exceptions.no_location_found_error import NoLocationFoundError
from app.services.location_resolver_service import LocationResolverService



class TestLocationResolverService(unittest.TestCase):
    def setUp(self):
        self.mock_get_latitude_longitude_address = Mock()
        self.service: LocationResolverService = LocationResolverService(self.mock_get_latitude_longitude_address)

    
    def test_location_resolver_success(self):
        address_input: str = 'Sverigestraße 1A'

        latitude: float = 48.2538614
        longitude: float = 16.4716313
        address: str = 'Sverigestraße 1a'
        self.mock_get_latitude_longitude_address.return_value = (latitude, longitude, address)

        result = self.service.run(address_input)

        self.mock_get_latitude_longitude_address.assert_called_once_with(address_input)
        self.assertEqual(result, Location(address=address, latitude=latitude, longitude=longitude))


    def test_location_resolver_location_fetch_error(self):
        address_input: str = 'Sverigestraße 1A'
        self.mock_get_latitude_longitude_address.side_effect = LocationFetchError(address_input, 400, 'Bad Request')

        with self.assertRaises(LocationFetchError):
            self.service.run(address_input)

    
    def test_location_resolver_no_location_found_error(self):
        address_input: str = 'Unkown Address'
        self.mock_get_latitude_longitude_address.side_effect = NoLocationFoundError(address_input)

        with self.assertRaises(NoLocationFoundError):
            self.service.run(address_input)