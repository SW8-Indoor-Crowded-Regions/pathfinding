import pytest
from app.classes.sensor import Sensor
from app.classes.room import Room
from app.classes.sensor_graph import SensorGraph

class TestSensorGraph:
    @pytest.fixture
    def sensors_and_rooms(self):
        # Create two dummy rooms.
        room1 = Room("room1", "Room A", 5)
        room2 = Room("room2", "Room B", 3)
        # Create dummy sensors and assign rooms manually.
        sensor1 = Sensor("sensor1", [])
        sensor1.rooms = [room1]
        sensor2 = Sensor("sensor2", [])
        sensor2.rooms = [room1, room2]
        sensor3 = Sensor("sensor3", [])
        sensor3.rooms = [room2]
        sensor4 = Sensor("sensor4", [])
        sensor4.rooms = []  # Sensor with no rooms.
        return [sensor1, sensor2, sensor3, sensor4], (room1, room2)

    def test_build_graph_nodes(self, sensors_and_rooms):
        sensors, _ = sensors_and_rooms
        graph_obj = SensorGraph(sensors)
        graph = graph_obj.build_graph()
        # Each sensor should be added as a node.
        for sensor in sensors:
            assert sensor.id in graph.nodes
            assert graph.nodes[sensor.id]['sensor'] == sensor

    def test_build_graph_edges(self, sensors_and_rooms):
        sensors, (room1, room2) = sensors_and_rooms
        graph_obj = SensorGraph(sensors)
        graph = graph_obj.build_graph()
        # sensor1 and sensor2 share room1.
        assert graph.has_edge("sensor1", "sensor2")
        # sensor2 and sensor3 share room2.
        assert graph.has_edge("sensor2", "sensor3")
        # sensor4, which belongs to no room, should have no connecting edges.
        assert list(graph.adj["sensor4"]) == []

    def test_edge_with_multiple_shared_rooms(self):
        # Two sensors sharing two different rooms.
        room1 = Room("room1", "Room A", 5)
        room2 = Room("room2", "Room B", 3)
        sensor1 = Sensor("sensor1", [])
        sensor1.rooms = [room1, room2]
        sensor2 = Sensor("sensor2", [])
        sensor2.rooms = [room1, room2]
        sensors = [sensor1, sensor2]
        graph_obj = SensorGraph(sensors)
        graph = graph_obj.build_graph()
        # Verify the edge exists.
        assert graph.has_edge("sensor1", "sensor2")
        edge_data = graph.get_edge_data("sensor1", "sensor2")
        # With two shared rooms, the edge data should have been converted to a weights list.
        assert 'weights' in edge_data
        # The weights list should contain both room crowd factors.
        assert sorted(edge_data['weights']) == sorted([5, 3])

    def test_edge_append_weights(self):
        # Two sensors sharing three different rooms.
        # This scenario will trigger the branch where after converting the first edge to a weights list,
        # a subsequent common room will cause the weights list to be appended.
        room1 = Room("room1", "Room A", 1)
        room2 = Room("room2", "Room B", 2)
        room3 = Room("room3", "Room C", 3)
        sensor1 = Sensor("sensor1", [])
        sensor2 = Sensor("sensor2", [])
        # Both sensors share three rooms.
        sensor1.rooms = [room1, room2, room3]
        sensor2.rooms = [room1, room2, room3]
        sensors = [sensor1, sensor2]
        graph_obj = SensorGraph(sensors)
        graph = graph_obj.build_graph()
        # Verify that an edge exists between sensor1 and sensor2.
        assert graph.has_edge("sensor1", "sensor2")
        edge_data = graph.get_edge_data("sensor1", "sensor2")
        # The edge data should now contain a 'weights' list.
        # Processing order:
        #   - First room: edge added with weight=1.
        #   - Second room: conversion to list -> [1, 2].
        #   - Third room: append branch is executed -> [1, 2, 3].
        assert 'weights' in edge_data
        assert edge_data['weights'] == [1, 2, 3]

    def test_find_fastest_path_valid(self):
        # Create three sensors connected through the same room.
        room = Room("room1", "Room A", 2)
        sensor1 = Sensor("sensor1", [])
        sensor1.rooms = [room]
        sensor2 = Sensor("sensor2", [])
        sensor2.rooms = [room]
        sensor3 = Sensor("sensor3", [])
        sensor3.rooms = [room]
        sensors = [sensor1, sensor2, sensor3]
        graph_obj = SensorGraph(sensors)
        graph_obj.build_graph()
        path, distance = graph_obj.find_fastest_path("sensor1", "sensor3")
        assert path is not None
        # Expected direct edge weight is 2.
        assert distance == 2

    def test_find_fastest_path_no_path(self):
        # Two sensors with no shared rooms.
        sensor1 = Sensor("sensor1", [])
        sensor1.rooms = []
        sensor2 = Sensor("sensor2", [])
        sensor2.rooms = []
        sensors = [sensor1, sensor2]
        graph_obj = SensorGraph(sensors)
        graph_obj.build_graph()
        path, distance = graph_obj.find_fastest_path("sensor1", "sensor2")
        assert path is None
        assert distance is None
