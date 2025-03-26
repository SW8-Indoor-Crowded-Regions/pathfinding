import time
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
    
    sensor_graph = SensorGraph(sensors)
    sensor_graph.build_graph()
    
    if not sensor_graph.graph.has_node(source_sensor):
        raise ValueError(f"Source sensor '{source_sensor}' not found in the sensor graph.")
    if not sensor_graph.graph.has_node(target_sensor):
        raise ValueError(f"Target sensor '{target_sensor}' not found in the sensor graph.")

    path, distance = sensor_graph.find_fastest_path(source_sensor, target_sensor)

    if not path or not distance:
        raise ValueError('No path found between the given sensors.')

    return {'fastest_path': path, 'distance': distance}
