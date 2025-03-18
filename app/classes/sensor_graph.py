import networkx as nx

class SensorGraph:
    def __init__(self, sensors: list):
        self.sensors = sensors
        self.graph = nx.Graph()

    def build_graph(self):
        """
        Builds a graph where each sensor is a node and an edge is added between
        sensors sharing a common room. The room’s crowd_factor is used as the weight.
        """
        # Add each sensor as a node.
        for sensor in self.sensors:
            self.graph.add_node(sensor.id, sensor=sensor)

        # Group sensors by the rooms they belong to.
        room_to_sensors = {}
        for sensor in self.sensors:
            for room in sensor.rooms:
                room_id = str(room.id)
                if room_id not in room_to_sensors:
                    room_to_sensors[room_id] = {'room': room, 'sensors': []}
                room_to_sensors[room_id]['sensors'].append(sensor)

        # Create edges between sensors that share the same room.
        for room_info in room_to_sensors.values():
            room = room_info['room']
            sensors_in_room = room_info['sensors']
            weight = room.crowd_factor  # Use room's crowd_factor as edge weight.
            for i in range(len(sensors_in_room)):
                for j in range(i + 1, len(sensors_in_room)):
                    sensor1 = sensors_in_room[i]
                    sensor2 = sensors_in_room[j]
                    if self.graph.has_edge(sensor1.id, sensor2.id):
                        if 'weights' in self.graph[sensor1.id][sensor2.id]:
                            self.graph[sensor1.id][sensor2.id]['weights'].append(weight)
                        else:
                            # Convert existing weight to a list of weights.
                            existing_weight = self.graph[sensor1.id][sensor2.id].pop('weight')
                            self.graph[sensor1.id][sensor2.id]['weights'] = [existing_weight, weight]
                    else:
                        self.graph.add_edge(sensor1.id, sensor2.id, weight=weight)
        return self.graph

    def find_fastest_path(self, source, target):
        """
        Uses Dijkstra's algorithm to find the fastest path between two sensors.
        The weight for each edge is taken from the destination room's 'crowdfactor' attribute.
        If a room does not have a 'crowdfactor', a default value of 1 is used.
        """
        def weight_func(u, v, d):
            if 'weights' in d:
                return sum(d['weights'])
            else:
                return d['weight']

        try:
            path = nx.dijkstra_path(self.graph, source, target, weight=weight_func)
            distance = nx.dijkstra_path_length(self.graph, source, target, weight=weight_func)
            return path, distance
        except nx.NetworkXNoPath:
            return None, None
