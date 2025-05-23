import networkx as nx
from collections import defaultdict
import itertools
import math


class SensorGraph:
	def __init__(self, sensors: list):
		self.sensors = sensors
		self.graph = nx.Graph()
		self._sensor_map = {s.id: s for s in sensors}

	def build_graph(self):
		"""
		Builds a Graph where each sensor is a node.
		For each room, an edge is added between every pair of sensors in that room.
		Each edge is assigned a weight equal to the room's calculate_weight().
		If two sensors share more than one room, only the first added edge is kept.
		"""
		for sensor in self.sensors:
			self.graph.add_node(sensor.id, sensor=sensor)

		room_to_sensors = defaultdict(list)
		room_info = {}
		for sensor_obj in self.sensors:
			for room_obj in sensor_obj.rooms:
				room_to_sensors[room_obj.id].append(sensor_obj)
				if room_obj.id not in room_info:
					room_info[room_obj.id] = room_obj

		previous_room_floor_value = None

		for room_id, sensor_list in room_to_sensors.items():
			current_room = room_info[room_id]

			floor_penalty_multiplier = 1.0
			if previous_room_floor_value is not None:
				if current_room.floor != previous_room_floor_value:
					floor_penalty_multiplier = 2.0

			for sensor1, sensor2 in itertools.combinations(sensor_list, 2):
				if not self.graph.has_edge(sensor1.id, sensor2.id):
					sensor_distance = sensor1.calculate_distance(sensor2)
					base_room_weight = current_room.calculate_weight()

					final_weight = (sensor_distance * base_room_weight) * floor_penalty_multiplier

					self.graph.add_edge(
						sensor1.id,
						sensor2.id,
						weight=final_weight,
						room_id=room_id,
					)

			previous_room_floor_value = current_room.floor

		return self.graph

	def attach_rooms(self, rooms_to_add: list):
		"""
		Attaches a room node to all its sensors in the graph with weight 0.
		Expects a list of Room objects.
		"""
		for sensor in self.sensors:
			for room in sensor.rooms:
				if room.id in rooms_to_add:
					self.graph.add_edge(sensor.id, room.id, weight=0, room_id=room.id)

	def _get_path_coordinates(self, node_path: list, rooms_to_exclude: set):
		"""Helper to convert a node path (including rooms/sensors) to sensor coordinates."""
		path_with_coordinates = []
		for node_id in node_path:
			if (
				node_id not in rooms_to_exclude
				and self.graph.has_node(node_id)
				and 'sensor' in self.graph.nodes[node_id]
			):
				sensor_obj = self.graph.nodes[node_id]['sensor']
				path_with_coordinates.append(sensor_obj)
		return path_with_coordinates

	def find_fastest_path(self, source: str, target: str):
		"""
		Uses Dijkstra's algorithm to find the fastest path between two nodes (rooms or sensors).
		Returns:
		    - List of intermediate sensor objects (excluding source/target rooms/sensors).
		    - Total distance (weight) of the path.
		    - The full list of node IDs in the path (including source/target).
		Raises:
		    nx.NetworkXNoPath: If no path exists between source and target.
		    KeyError: If source or target node does not exist in the graph.
		"""
		try:
			path_nodes = nx.dijkstra_path(self.graph, source, target, weight='weight')
			distance = nx.dijkstra_path_length(self.graph, source, target, weight='weight')

			path_with_coordinates = self._get_path_coordinates(path_nodes, {source, target})

			return path_with_coordinates, distance
		except (nx.NetworkXNoPath, KeyError) as e:
			raise e

	def find_multi_point_path_nearest_neighbor(self, source_room: str, target_rooms: list[str]):
		"""
		Finds a path starting at source_room, visiting all target_rooms using the
		Nearest Neighbor heuristic based on Dijkstra path lengths.

		Args:
		    source_room (str): The ID of the starting room.
		    target_rooms (list or set): A collection of target room IDs to visit.

		Returns:
		    tuple: (ordered_rooms_visited, full_sensor_path_coords, total_distance)
		        - ordered_rooms_visited (list): The sequence of rooms visited, starting with source_room.
		        - full_sensor_path_coords (list): A list of sensor objects for the entire path.
		        - total_distance (float): The total accumulated weight/distance of the path.

		Raises:
		    ValueError: If source or any target room is not in the graph, or if no path can be found
		                between consecutive points in the tour.
		"""
		unvisited_targets = set(target_rooms) - {source_room}

		current_room = source_room
		ordered_rooms_visited = [source_room]
		full_node_path = [source_room]
		total_distance = 0.0

		while unvisited_targets:
			nearest_target = None
			shortest_segment_distance = math.inf

			for target in unvisited_targets:
				try:
					distance = nx.dijkstra_path_length(
						self.graph, current_room, target, weight='weight'
					)
					if distance < shortest_segment_distance:
						shortest_segment_distance = distance
						nearest_target = target
				except nx.NetworkXNoPath:
					raise ValueError('No path found between the given rooms.')
				except KeyError:
					raise ValueError(
						f"Node '{current_room}' or '{target}' not found in graph during NN search."
					)

			if nearest_target is None:
				raise ValueError(
					f"Could not find nearest neighbor from '{current_room}' among remaining targets: {unvisited_targets}"
				)

			try:
				segment_nodes = nx.dijkstra_path(
					self.graph, current_room, nearest_target, weight='weight'
				)
			except (nx.NetworkXNoPath, KeyError):
				raise ValueError('No path found between the given rooms after distance check.')

			full_node_path.extend(segment_nodes[1:])
			total_distance += shortest_segment_distance
			current_room = nearest_target
			ordered_rooms_visited.append(current_room)
			unvisited_targets.remove(current_room)

		all_tour_rooms = set(ordered_rooms_visited)
		full_sensor_path_coords = self._get_path_coordinates(full_node_path, all_tour_rooms)

		return full_sensor_path_coords, total_distance
