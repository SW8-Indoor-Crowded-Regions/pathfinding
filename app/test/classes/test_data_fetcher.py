import pytest
import requests
from app.classes.data_fetcher import DataFetcher
from app.classes.sensor import Sensor
from app.classes.room import Room

class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError("Error occurred")

class TestDataFetcher:
    def fake_requests_get(self, url):
        # Return a fake response based on the endpoint.
        if "sensors" in url:
            return FakeResponse({"sensors": [
                {"id": "sensor1", "rooms": ["room1"]},
                {"id": "sensor2", "rooms": []}
            ]})
        elif "rooms" in url:
            return FakeResponse({"rooms": [
                {"id": "room1", "name": "Room A", "crowd_factor": 5}
            ]})
        return FakeResponse({})

    def test_get_sensors(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.fake_requests_get)
        fetcher = DataFetcher(base_url="http://dummy")
        sensors = fetcher.get_sensors()
        assert len(sensors) == 2
        assert sensors[0].id == "sensor1"
        assert sensors[0].room_ids == ["room1"]

    def test_get_rooms(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.fake_requests_get)
        fetcher = DataFetcher(base_url="http://dummy")
        rooms = fetcher.get_rooms()
        assert len(rooms) == 1
        assert rooms[0].id == "room1"
        assert rooms[0].name == "Room A"
        assert rooms[0].crowd_factor == 5
