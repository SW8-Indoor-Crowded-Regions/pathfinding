from ..classes.room import Room
from ..classes.sensor import Sensor
from ..classes.sensor_graph import SensorGraph
from ..schemas.path import FastestPathRequest

def create_fastest_path(request_body: FastestPathRequest):
    """
    Processes a FastestPathRequest to compute the fastest path using a sensor graph.
    Raises:
        ValueError: If source or target room is not found or no path can be found.
    """
    rooms = Room.create_room_mapping_from_schemas(request_body.rooms or [])
    sensors = Sensor.create_sensors_from_schemas(request_body.sensors or [], rooms)

    source_room = request_body.source_room
    target_room = request_body.target_room
    
    sensor_graph = SensorGraph(sensors)
    sensor_graph.build_graph()
    
    sensor_graph.attach_room(source_room)
    sensor_graph.attach_room(target_room)
    
    if not sensor_graph.graph.has_node(source_room):
        raise ValueError(f"Source room '{source_room}' not found in the sensor graph.")
    if not sensor_graph.graph.has_node(target_room):
        raise ValueError(f"Target room '{target_room}' not found in the sensor graph.")

    path, distance = sensor_graph.find_fastest_path(source_room, target_room)

    if not path:
        raise ValueError('No path found between the given rooms.')

    return {'fastest_path': path, 'distance': distance}
