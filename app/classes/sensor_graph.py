import networkx as nx
from collections import defaultdict
import itertools


class SensorGraph:
    def __init__(self, sensors: list):
        self.sensors = sensors
        # Use a simple Graph to ensure a single edge per sensor pair.
        self.graph = nx.Graph()

    def build_graph(self):
        """
        Builds a Graph where each sensor is a node.
        For each room, an edge is added between every pair of sensors in that room.
        Each edge is assigned a weight equal to the room's crowd_factor.
        If two sensors share more than one room, only the first added edge is kept.
        """
        # Add each sensor as a node.
        for sensor in self.sensors:
            self.graph.add_node(sensor.id, sensor=sensor)

        # Group sensors by room.
        room_to_sensors = defaultdict(list)
        room_info = {}
        for sensor in self.sensors:
            for room in sensor.rooms:
                room_to_sensors[room.id].append(sensor)
                room_info[room.id] = room  # store room info for crowd_factor

        # For each room, add an edge between every pair of sensors in that room.
        for room_id, sensor_list in room_to_sensors.items():
            room = room_info[room_id]
            for sensor1, sensor2 in itertools.combinations(sensor_list, 2):
                # If an edge already exists between these sensors, ignore the new one.
                if not self.graph.has_edge(sensor1.id, sensor2.id):
                    self.graph.add_edge(
                        sensor1.id, sensor2.id, weight=room.calculate_weight(), room_id=room_id
                    )
        return self.graph

    def find_fastest_path(self, source, target):
        """
        Uses Dijkstra's algorithm to find the fastest path between two sensors
        based solely on the edge weight of the room connecting them.
        """
        try:
            path = nx.dijkstra_path(self.graph, source, target, weight='weight')
            distance = nx.dijkstra_path_length(self.graph, source, target, weight='weight')
            return path, distance
        except nx.NetworkXNoPath:
            return None, None
