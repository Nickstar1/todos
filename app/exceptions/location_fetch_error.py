class LocationFetchError(Exception):
    def __init__(self, address: str, status_code: int, response_text: str):
        super().__init__(f'could not fetch latitude/longitude for address: {address}\nstatus code: {status_code}\nresponse text: {response_text}')