from ..classes.room import Room
from ..classes.sensor import Sensor
from ..classes.sensor_graph import SensorGraph
from ..schemas.path import FastestPathRequest


def create_fastest_path(request_body: FastestPathRequest):
	"""
	Processes a FastestPathRequest to compute the fastest path using a sensor graph.
	Raises:
	    ValueError: If source or target room is not found or no path can be found.
	"""
	rooms = Room.create_room_mapping_from_schemas(request_body.rooms or [])
	sensors = Sensor.create_sensors_from_schemas(request_body.sensors or [], rooms)

	source_room = request_body.source_room
	target_room = request_body.target_room

	sensor_graph = SensorGraph(sensors)
	sensor_graph.build_graph()

	sensor_graph.attach_room(source_room)
	sensor_graph.attach_room(target_room)

	if not sensor_graph.graph.has_node(source_room) or not check_room_is_valid(source_room, rooms):
		raise ValueError(f"Source room '{source_room}' is not valid.")
	if not sensor_graph.graph.has_node(target_room) or not check_room_is_valid(target_room, rooms):
		raise ValueError(f"Target room '{target_room}' is not valid.")

	path, distance = sensor_graph.find_fastest_path(source_room, target_room)

	if not path:
		raise ValueError('No path found between the given rooms.')

	return {'fastest_path': path, 'distance': distance}


def check_room_is_valid(room: str, rooms: list[str]) -> bool:
	"""
	Checks if a room is valid by verifying its presence in the list of rooms.
	Args:
	    room (str): The room to check.
	    rooms (list[str]): The list of valid rooms.
	Returns:
	    bool: True if the room is valid, False otherwise.
	"""
	return room in rooms
