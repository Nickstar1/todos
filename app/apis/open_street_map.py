
from typing import Any, Dict, List, Tuple

import requests
from requests import Response

from app.exceptions.location_fetch_error import LocationFetchError
from app.exceptions.no_location_found_error import NoLocationFoundError

LocationData = Dict[str, Any]

def get_latitude_longitude_address(address: str) -> Tuple[float, float, str]:
    url = 'https://nominatim.openstreetmap.org/search'
    params: dict[str, str] = {
        'q': address,
        'format': 'json',
        'limit': '1',
        'addressdetails': '1'
    }
    headers: dict[str, str] = {'User-Agent': 'todos-app/1.0'}

    response: Response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise LocationFetchError(address, response.status_code, response.text)

    data: List[LocationData] = response.json()

    if not data:
        raise NoLocationFoundError(address)
    
    street: str = data[0]['address']['road']
    house_number: str = data[0]['address'].get('house_number', '') 
    address: str = f'{street} {house_number}'
    
    return (float(data[0]['lat']), float(data[0]['lon']), address)