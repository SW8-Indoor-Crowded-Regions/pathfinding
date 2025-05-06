from ..classes.room import Room
from ..classes.sensor import Sensor
from ..classes.sensor_graph import SensorGraph
from ..schemas.path import FastestPathRequest, MultiplePointsRequest
import networkx as nx


def check_room_id_is_valid(room_id: str, room_mapping: dict) -> bool:
	"""
	Checks if a room ID exists as a key in the room mapping.
	Args:
	    room_id (str): The room ID to check.
	    room_mapping (dict): The dictionary mapping room IDs to Room objects.
	Returns:
	    bool: True if the room ID is valid, False otherwise.
	"""
	return room_id in room_mapping


def create_fastest_path(request_body: FastestPathRequest):
	"""
	Processes a FastestPathRequest to compute the fastest path using a sensor graph.
	Raises:
	    ValueError: If source or target room is not found or no path can be found.
	"""
	room_mapping = Room.create_room_mapping_from_schemas(request_body.rooms or [])

	sensors = Sensor.create_sensors_from_schemas(request_body.sensors or [], room_mapping)

	source_room_id = request_body.source_room
	target_room_id = request_body.target_room

	if not check_room_id_is_valid(source_room_id, room_mapping):
		raise ValueError(f"Source room '{source_room_id}' is not valid.")
	if not check_room_id_is_valid(target_room_id, room_mapping):
		raise ValueError(f"Target room '{target_room_id}' is not valid.")

	sensor_graph = SensorGraph(sensors)
	sensor_graph.build_graph()

	sensor_graph.attach_rooms([source_room_id, target_room_id])

	if not sensor_graph.graph.has_node(source_room_id):
		raise ValueError(
			f"Source room '{source_room_id}' is not connected to any sensor in the graph."
		)
	if not sensor_graph.graph.has_node(target_room_id):
		raise ValueError(
			f"Target room '{target_room_id}' is not connected to any sensor in the graph."
		)

	try:
		path_sensors, distance = sensor_graph.find_fastest_path(source_room_id, target_room_id)

		return {'fastest_path': path_sensors, 'distance': distance}
	except nx.NetworkXNoPath:
		raise ValueError('No path found between the given rooms.')
	except KeyError as e:
		raise ValueError(f'Graph error: Node {e} not found during pathfinding.')


def create_multiple_points_path(request_body: MultiplePointsRequest):
	"""
	Finds a path visiting multiple target rooms starting from a source room
	using the Nearest Neighbor heuristic on a sensor graph.

	Raises:
	    ValueError: If source or target rooms are invalid, not found in the graph,
	                or if a path cannot be completed between required points.
	"""
	room_mapping = Room.create_room_mapping_from_schemas(request_body.rooms or [])

	sensors = Sensor.create_sensors_from_schemas(request_body.sensors or [], room_mapping)

	source_room_id = request_body.source_room
	target_room_ids = list(set(request_body.target_rooms) - {source_room_id})

	if not target_room_ids:
		raise ValueError(
			'Target rooms list must contain at least one room different from the source room.'
		)

	all_room_ids_in_tour = [source_room_id] + target_room_ids
	for room_id in all_room_ids_in_tour:
		if not check_room_id_is_valid(room_id, room_mapping):
			raise ValueError(f"Room '{room_id}' in the tour is not valid.")

	sensor_graph = SensorGraph(sensors)
	sensor_graph.build_graph()

	sensor_graph.attach_rooms(all_room_ids_in_tour)

	for room_id in all_room_ids_in_tour:
		if not sensor_graph.graph.has_node(room_id):
			raise ValueError(f"Room '{room_id}' is not connected to any sensor in the graph.")

	try:
		sensor_objects_path, total_distance = sensor_graph.find_multi_point_path_nearest_neighbor(
			source_room_id,
			target_room_ids,
		)

		return {'fastest_path': sensor_objects_path, 'distance': total_distance}
	except (ValueError, nx.NetworkXNoPath, KeyError) as e:
		raise ValueError(f'Failed to compute multi-point path: {e}')
