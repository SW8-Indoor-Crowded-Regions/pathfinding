from app.classes.sensor import Sensor
from app.classes.room import Room
import types


class TestSensor:
	def test_sensor_creation_from_schema_object_with_valid_room_id(self):
		room1 = Room(
			id='room1',
			name='Room A',
			occupants=5,
			area=100.0,
			crowd_factor=200.0,
			popularity_factor=1.2,
		)
		room_mapping = {'room1': room1}

		schema_data = {'id': 'sensor1', 'longitude': 10.0, 'latitude': 20.0, 'is_vertical': False, 'rooms': ['room1']}
		schema_object = types.SimpleNamespace(**schema_data)

		sensor = Sensor.from_schema(schema=schema_object, room_mapping=room_mapping)

		assert len(sensor.rooms) == 1
		assert sensor.rooms[0] == room1
		assert sensor.rooms[0].id == 'room1'

	def test_sensor_initialization_directly_with_room_objects(self):
		room1 = Room(
			id='room_init',
			name='Init Room',
			occupants=1,
			area=10,
			crowd_factor=0.1,
			popularity_factor=1,
		)
		sensor = Sensor(id='sensor_init', longitude=0.0, latitude=0.0, is_vertical=True, rooms=[room1])
		assert len(sensor.rooms) == 1
		assert sensor.rooms[0] == room1
