from ..classes.room import Room
from ..classes.sensor import Sensor
from ..classes.sensor_graph import SensorGraph
from ..schemas.path import FastestPathRequest, MultiplePointsRequest
import networkx as nx


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

	sensor_graph.attach_rooms([source_room, target_room])

	if not sensor_graph.graph.has_node(source_room) or not check_room_is_valid(source_room, rooms):
		raise ValueError(f"Source room '{source_room}' is not valid.")
	if not sensor_graph.graph.has_node(target_room) or not check_room_is_valid(target_room, rooms):
		raise ValueError(f"Target room '{target_room}' is not valid.")

	try:
		# Use the updated find_fastest_path which might raise exceptions
		path_coords, distance, _ = sensor_graph.find_fastest_path(source_room, target_room)
		# find_fastest_path now raises exceptions directly if no path or key error
		return {'fastest_path': path_coords, 'distance': distance}
	except (nx.NetworkXNoPath, KeyError) as e:
			# Catch exceptions from find_fastest_path
			raise ValueError(f"No path found between '{source_room}' and '{target_room}': {e}")


def create_multiple_points_path(request_body: MultiplePointsRequest):
    """
    Finds a path visiting multiple target rooms starting from a source room
    using the Nearest Neighbor heuristic on a sensor graph.

    Raises:
        ValueError: If source or target rooms are invalid, not found in the graph,
                    or if a path cannot be completed between required points.
    """
    rooms = Room.create_room_mapping_from_schemas(request_body.rooms or [])
    sensors = Sensor.create_sensors_from_schemas(request_body.sensors or [], rooms)

    source_room = request_body.source_room
    # Ensure target_rooms is a list and remove duplicates/source
    target_rooms = list(set(request_body.target_rooms) - {source_room})

    if not target_rooms:
        raise ValueError("Target rooms list cannot be empty or only contain the source room.")

    sensor_graph = SensorGraph(sensors)
    sensor_graph.build_graph()

    # Attach source and all unique target rooms to the graph
    all_rooms_in_tour = [source_room] + target_rooms
    sensor_graph.attach_rooms(all_rooms_in_tour)

    # Validation (after attaching nodes)
    if not sensor_graph.graph.has_node(source_room) or not check_room_is_valid(source_room, rooms):
         raise ValueError(f"Source room '{source_room}' is not valid or not connected in the graph.")
    for target_room in target_rooms:
         if not sensor_graph.graph.has_node(target_room) or not check_room_is_valid(target_room, rooms):
             raise ValueError(f"Target room '{target_room}' is not valid or not connected in the graph.")

    # Find the path using the nearest neighbor method
    try:
        ordered_rooms, sensor_coords_path, total_distance = sensor_graph.find_multi_point_path_nearest_neighbor(
            source_room, target_rooms
        )

        return {
            'ordered_rooms_visited': ordered_rooms,
            'sensor_path': sensor_coords_path,
            'total_distance': total_distance
        }
    except (ValueError, nx.NetworkXNoPath, KeyError) as e:
         # Catch errors during the nearest neighbor calculation
         raise ValueError(f"Failed to compute multi-point path: {e}")


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
