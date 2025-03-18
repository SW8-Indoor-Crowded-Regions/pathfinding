import requests
from .room import Room
from .sensor import Sensor

class DataFetcher:
    def __init__(self, base_url="http://localhost:8002"):
        self.base_url = base_url

    def fetch_data(self, endpoint: str):
        """
        Fetch JSON data from the given endpoint.
        """
        url = f"{self.base_url}/{endpoint}/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_sensors(self) -> list:
        """
        Retrieve sensors from the API and convert them into Sensor objects.
        """
        data = self.fetch_data("sensors")
        sensors_list = data["sensors"] if isinstance(data, dict) and "sensors" in data else data
        return [Sensor.from_dict(sensor) for sensor in sensors_list]

    def get_rooms(self) -> list:
        """
        Retrieve rooms from the API and convert them into Room objects.
        """
        data = self.fetch_data("rooms")
        rooms_list = data["rooms"] if isinstance(data, dict) and "rooms" in data else data
        return [Room.from_dict(room) for room in rooms_list]
