import os
from ..classes.room import Room
from ..classes.sensor import Sensor
from ..classes.sensor_graph import SensorGraph
from ..schemas.path import FastestPathRequest

def create_fastest_path(request_body: FastestPathRequest):
    """
    Processes a FastestPathRequest to compute the fastest path using a sensor graph.
    Raises:
        ValueError: If source or target sensor is not found or no path can be found.
    """
    rooms = Room.create_room_mapping_from_schemas(request_body.rooms or [])
    sensors = Sensor.create_sensors_from_schemas(request_body.sensors or [], rooms)

    source_sensor = request_body.source_sensor
    target_sensor = request_body.target_sensor

    if source_sensor not in [s.id for s in sensors]:
        raise ValueError(f"Source sensor '{source_sensor}' not found in sensor list.")
    if target_sensor not in [s.id for s in sensors]:
        raise ValueError(f"Target sensor '{target_sensor}' not found in sensor list.")

    graph_filename = r"C:\\Github\\SW8\\pathfinding\\app\\sensor_graph.pickle"

    sensor_graph = SensorGraph(sensors)
    if os.path.exists(graph_filename):
        try:
            sensor_graph.load_graph(graph_filename)
        except Exception:
            sensor_graph.build_graph()
            sensor_graph.save_graph(graph_filename)
    else:
        sensor_graph.build_graph()
        sensor_graph.save_graph(graph_filename)

    path, distance = sensor_graph.find_fastest_path(source_sensor, target_sensor)

    if not path or not distance:
        raise ValueError("No path found between the given sensors.")

    return {
        "fastest_path": path,
        "distance": distance
    }
