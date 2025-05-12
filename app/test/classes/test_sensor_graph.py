import pytest
import networkx as nx
from app.classes.sensor import Sensor
from app.classes.room import Room
from app.classes.sensor_graph import SensorGraph


class TestSensorGraph:
	@pytest.fixture
	def sensors_and_rooms(self):
		room1 = Room('room1', 'Room A', 5, 100, 200, 1.2, 1)
		room2 = Room('room2', 'Room B', 3, 50, 150, 1.3, 1)
		room3 = Room('room3', 'Room C', 4, 75, 175, 1.1, 2)
		room4 = Room('room4', 'Room D', 6, 125, 225, 1.8, 3)
		room5 = Room('room5', 'Room E', 7, 150, 250, 1.4, 4)

		sensor1 = Sensor(id='sensor1', rooms=[], latitude=12.34, longitude=56.78, is_vertical=True)
		sensor1.rooms = [room1, room2]
		sensor2 = Sensor(id='sensor2', rooms=[], latitude=12.34, longitude=56.78, is_vertical=True)
		sensor2.rooms = [room1, room3]
		sensor3 = Sensor(id='sensor3', rooms=[], latitude=12.34, longitude=56.78, is_vertical=True)
		sensor3.rooms = [
			room2,
			room3,
		]

		sensor4 = Sensor('sensor4', 12.34, 56.78, True, [])
		sensor4.rooms = [room4, room5]

		return [sensor1, sensor2, sensor3, sensor4], (room1, room2, room3, room4, room5)

	def test_build_graph_nodes(self, sensors_and_rooms):
		sensors, _ = sensors_and_rooms
		for sensor in sensors:
			assert len(sensor.rooms) == 2, f'Sensor {sensor.id} does not have exactly 2 rooms.'

		graph_obj = SensorGraph(sensors)
		graph = graph_obj.build_graph()
		for sensor in sensors:
			assert sensor.id in graph.nodes
			assert graph.nodes[sensor.id]['sensor'] == sensor

	def test_build_graph_edges(self, sensors_and_rooms):
		sensors, (room1, room2, room3, room4, room5) = sensors_and_rooms
		graph_obj = SensorGraph(sensors)
		graph = graph_obj.build_graph()
		assert graph.has_edge('sensor1', 'sensor2')
		assert graph.has_edge('sensor1', 'sensor3')
		assert graph.has_edge('sensor2', 'sensor3')
		assert list(graph.adj['sensor4']) == []

	def test_edge_with_multiple_shared_rooms(self):
		room1 = Room('room1', 'Room A', 5, 100, 200, 1.9, 1)
		room2 = Room('room2', 'Room B', 3, 50, 150, 0.9, 1)
		sensor1 = Sensor('sensor1', 12.34, 56.78, True, [])
		sensor1.rooms = [room1, room2]
		sensor2 = Sensor('sensor2', 12.34, 56.78, True, [])
		sensor2.rooms = [room1, room2]
		sensors = [sensor1, sensor2]
		graph_obj = SensorGraph(sensors)
		graph = graph_obj.build_graph()
		assert graph.has_edge('sensor1', 'sensor2')
		edge_data = graph.get_edge_data('sensor1', 'sensor2')
		assert 'weight' in edge_data
		assert edge_data['weight'] == sensor1.calculate_weight_haversine(sensor2) * room1.calculate_weight()

	def test_find_fastest_path_valid(self):
		room1 = Room('room1', 'Room A', 2, 50, 100, 1.2, 1)
		room2 = Room('room2', 'Room B', 3, 75, 125, 1.2, 2)
		sensor1 = Sensor('sensor1', 12.34, 56.78, True, [])
		sensor1.rooms = [room1, room2]
		sensor2 = Sensor('sensor2', 12.34, 56.78, True, [])
		sensor2.rooms = [room1, room2]
		sensor3 = Sensor('sensor3', 12.34, 56.78, True, [])
		sensor3.rooms = [room1, room2]
		sensors = [sensor1, sensor2, sensor3]
		graph_obj = SensorGraph(sensors)
		graph_obj.build_graph()
		path, distance = graph_obj.find_fastest_path('sensor1', 'sensor3')
		assert path is not None
		assert isinstance(path, list)
		assert isinstance(distance, (int, float))

	def test_find_fastest_path_no_path(self):
		room1 = Room('room1', 'Room A', 2, 50, 100, 1.2, 1)
		room2 = Room('room2', 'Room B', 3, 75, 125, 1.2, 2)
		room3 = Room('room3', 'Room C', 4, 100, 150, 1.2, 3)
		room4 = Room('room4', 'Room D', 5, 125, 175, 1.2, 4)
		sensor1 = Sensor('sensor1', 12.34, 56.78, True, [])
		sensor1.rooms = [room1, room2]
		sensor2 = Sensor('sensor2', 12.34, 56.78, True, [])
		sensor2.rooms = [room3, room4]
		sensors = [sensor1, sensor2]
		graph_obj = SensorGraph(sensors)
		graph_obj.build_graph()
		with pytest.raises(nx.NetworkXNoPath):
			graph_obj.find_fastest_path('sensor1', 'sensor2')
