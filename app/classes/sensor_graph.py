import networkx as nx
import pickle
from collections import defaultdict
import itertools

class SensorGraph:
    def __init__(self, sensors: list):
        self.sensors = sensors
        # Use MultiGraph to allow multiple edges between the same pair of sensors.
        self.graph = nx.MultiGraph()

    def build_graph(self):
        """
        Builds a MultiGraph where each sensor is a node. For each room,
        an edge is added between every pair of sensors in that room.
        Each edge is assigned a weight equal to the room's crowd_factor.
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
                # Add an edge representing the pathway in this room.
                self.graph.add_edge(sensor1.id, sensor2.id, weight=room.crowd_factor, room_id=room_id)

        return self.graph

    def save_graph(self, filename: str):
        """
        Saves the current graph to a file using pickle.
        """
        with open(filename, "wb") as f:
            pickle.dump(self.graph, f)

    def load_graph(self, filename: str):
        """
        Loads a graph from a file using pickle.
        """
        with open(filename, "rb") as f:
            self.graph = pickle.load(f)
        return self.graph

    def find_fastest_path(self, source, target):
        """
        Uses Dijkstra's algorithm to find the fastest path between two sensors.
        Because the graph is a MultiGraph (possibly multiple edges between a pair),
        we first collapse it to a simple graph where, for each sensor pair, the edge weight
        is the minimum crowd_factor among the parallel edges.
        """
        simple_graph = nx.Graph()
        # For each edge in the MultiGraph, add the minimum weight edge to the simple graph.
        for u, v, data in self.graph.edges(data=True):
            w = data.get('weight', 1)  # default weight is 1 if not provided
            if simple_graph.has_edge(u, v):
                simple_graph[u][v]['weight'] = min(simple_graph[u][v]['weight'], w)
            else:
                simple_graph.add_edge(u, v, weight=w)
        try:
            path = nx.dijkstra_path(simple_graph, source, target, weight='weight')
            distance = nx.dijkstra_path_length(simple_graph, source, target, weight='weight')
            return path, distance
        except nx.NetworkXNoPath:
            return None, None
