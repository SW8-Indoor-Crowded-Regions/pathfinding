from app.classes.sensor import Sensor
from app.classes.room import Room


class TestSensor:
    def test_from_dict(self):
        data = {'id': 'sensor1', 'rooms': ['room1', 'room2'], 'longitude': 10.0, 'latitude': 20.0}
        sensor = Sensor.from_dict(data)
        assert sensor.id == 'sensor1'
        assert sensor.room_ids == ['room1', 'room2']
        # Initially, rooms list should be empty.
        assert sensor.rooms == []

    def test_attach_rooms_with_valid_and_invalid_ids(self):
        sensor = Sensor('sensor1', ['room1', 'roomX'], 10.0, 20.0)
        room1 = Room('room1', 'Room A', 5, 100, 200, 1.2)
        room_mapping = {'room1': room1}
        sensor.attach_rooms(room_mapping)
        # Only the valid room is attached.
        assert sensor.rooms == [room1]
