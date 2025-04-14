import pytest
from app.classes.sensor import Sensor
from app.classes.room import Room
from app.classes.sensor_graph import SensorGraph


class TestSensorGraph:
	@pytest.fixture
	def sensors_and_rooms(self):
		# Create five dummy rooms.
		room1 = Room('room1', 'Room A', 5, 100, 200, 1.2)
		room2 = Room('room2', 'Room B', 3, 50, 150, 1.3)
		room3 = Room('room3', 'Room C', 4, 75, 175, 1.1)
		room4 = Room('room4', 'Room D', 6, 125, 225, 1.8)
		room5 = Room('room5', 'Room E', 7, 150, 250, 1.4)

		# Create sensors with exactly two rooms each.
		# Sensors 1, 2, and 3 share rooms in a way that forms a connected subgraph.
		sensor1 = Sensor('sensor1', [], 12.34, 56.78)
		sensor1.rooms = [room1, room2]  # sensor1: room1 and room2
		sensor2 = Sensor('sensor2', [], 12.34, 56.78)
		sensor2.rooms = [room1, room3]  # sensor2: room1 and room3 (common with sensor1: room1)
		sensor3 = Sensor('sensor3', [], 12.34, 56.78)
		sensor3.rooms = [
			room2,
			room3,
		]  # sensor3: room2 and room3 (common with sensor1: room2, sensor2: room3)

		# Sensor4 is isolated by having a pair of rooms that no other sensor uses.
		sensor4 = Sensor('sensor4', [], 12.34, 56.78)
		sensor4.rooms = [room4, room5]

		return [sensor1, sensor2, sensor3, sensor4], (room1, room2, room3, room4, room5)

	def test_build_graph_nodes(self, sensors_and_rooms):
		sensors, _ = sensors_and_rooms
		# Assert that each sensor has exactly 2 rooms.
		for sensor in sensors:
			assert len(sensor.rooms) == 2, f'Sensor {sensor.id} does not have exactly 2 rooms.'

		graph_obj = SensorGraph(sensors)
		graph = graph_obj.build_graph()
		# Each sensor should be added as a node.
		for sensor in sensors:
			assert sensor.id in graph.nodes
			assert graph.nodes[sensor.id]['sensor'] == sensor

	def test_build_graph_edges(self, sensors_and_rooms):
		sensors, (room1, room2, room3, room4, room5) = sensors_and_rooms
		graph_obj = SensorGraph(sensors)
		graph = graph_obj.build_graph()
		# sensor1 and sensor2 share room1.
		assert graph.has_edge('sensor1', 'sensor2')
		# sensor1 and sensor3 share room2.
		assert graph.has_edge('sensor1', 'sensor3')
		# sensor2 and sensor3 share room3.
		assert graph.has_edge('sensor2', 'sensor3')
		# sensor4 is isolated; no other sensor shares room4 or room5.
		assert list(graph.adj['sensor4']) == []

	def test_edge_with_multiple_shared_rooms(self):
		# Create two sensors sharing exactly the same two rooms.
		room1 = Room('room1', 'Room A', 5, 100, 200, 1.9)
		room2 = Room('room2', 'Room B', 3, 50, 150, 0.9)
		sensor1 = Sensor('sensor1', [], 12.34, 56.78)
		sensor1.rooms = [room1, room2]
		sensor2 = Sensor('sensor2', [], 12.34, 56.78)
		sensor2.rooms = [room1, room2]
		sensors = [sensor1, sensor2]
		graph_obj = SensorGraph(sensors)
		graph = graph_obj.build_graph()
		# Verify the edge exists.
		assert graph.has_edge('sensor1', 'sensor2')
		edge_data = graph.get_edge_data('sensor1', 'sensor2')
		# Expect the edge's weight to be that of the first room in the sensor's room list.
		assert 'weight' in edge_data
		assert edge_data['weight'] == room1.calculate_weight()

	def test_find_fastest_path_valid(self):
		# Create three sensors that all share the same two rooms.
		room1 = Room('room1', 'Room A', 2, 50, 100, 1.2)
		room2 = Room('room2', 'Room B', 3, 75, 125, 1.2)
		sensor1 = Sensor('sensor1', [], 12.34, 56.78)
		sensor1.rooms = [room1, room2]
		sensor2 = Sensor('sensor2', [], 12.34, 56.78)
		sensor2.rooms = [room1, room2]
		sensor3 = Sensor('sensor3', [], 12.34, 56.78)
		sensor3.rooms = [room1, room2]
		sensors = [sensor1, sensor2, sensor3]
		graph_obj = SensorGraph(sensors)
		graph_obj.build_graph()
		path, distance = graph_obj.find_fastest_path('sensor1', 'sensor3')
		assert path is not None
		# Expected direct edge weight is that of room1 (the first room): 2.
		assert distance == 1.0

	def test_find_fastest_path_no_path(self):
		# Create two sensors with completely disjoint sets of rooms (each with 2 rooms).
		room1 = Room('room1', 'Room A', 2, 50, 100, 1.2)
		room2 = Room('room2', 'Room B', 3, 75, 125, 1.2)
		room3 = Room('room3', 'Room C', 4, 100, 150, 1.2)
		room4 = Room('room4', 'Room D', 5, 125, 175, 1.2)
		sensor1 = Sensor('sensor1', [], 12.34, 56.78)
		sensor1.rooms = [room1, room2]
		sensor2 = Sensor('sensor2', [], 12.34, 56.78)
		sensor2.rooms = [room3, room4]
		sensors = [sensor1, sensor2]
		graph_obj = SensorGraph(sensors)
		graph_obj.build_graph()
		path, distance = graph_obj.find_fastest_path('sensor1', 'sensor2')
		assert path is None
		assert distance is None
