import os
from ..classes.room import Room
from ..classes.sensor import Sensor
from ..classes.sensor_graph import SensorGraph
from ..schemas.path import FastestPathRequest

DEFAULT_GRAPH_PATH = "app/sensor_graph.pickle"

def create_fastest_path(request_body: FastestPathRequest, graph_path: str = DEFAULT_GRAPH_PATH):
    """
    Processes a FastestPathRequest to compute the fastest path using a sensor graph.
    Raises:
        ValueError: If source or target sensor is not found or no path can be found.
    """
    rooms = Room.create_room_mapping_from_schemas(request_body.rooms or [])
    sensors = Sensor.create_sensors_from_schemas(request_body.sensors or [], rooms)

    source_sensor = request_body.source_sensor
    target_sensor = request_body.target_sensor

    graph_filename = graph_path

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
    
    if not sensor_graph.graph.has_node(source_sensor):
        raise ValueError(f"Source sensor '{source_sensor}' not found in the sensor graph.")
    if not sensor_graph.graph.has_node(target_sensor):
        raise ValueError(f"Target sensor '{target_sensor}' not found in the sensor graph.")


    path, distance = sensor_graph.find_fastest_path(source_sensor, target_sensor)

    if not path or not distance:
        raise ValueError("No path found between the given sensors.")

    return {
        "fastest_path": path,
        "distance": distance
    }
