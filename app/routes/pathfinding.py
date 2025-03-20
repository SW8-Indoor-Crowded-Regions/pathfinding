from fastapi import APIRouter
from ..services.route_service import create_fastest_path
from ..schemas.path import PathRequest
from ..classes.room import Room
from ..classes.sensor import Sensor
from ..classes.sensor_graph import SensorGraph

router = APIRouter(prefix="/pathfinding")

@router.post("/fastest-path")
async def get_fastest_path(request_body: PathRequest):
    """
    Accepts a JSON payload containing lists of Rooms and Sensors, along with
    optional source/target sensor IDs for pathfinding.

    Example request body:
    {
      "rooms": [
         { "id": "roomA", "name": "Lobby", "crowd_factor": 2 },
         { "id": "roomB", "name": "Hallway", "crowd_factor": 1 },
         { "id": "roomC", "name": "Meeting Room", "crowd_factor": 3 }
      ],
      "sensors": [
         { "id": "sensor1", "rooms": ["roomA, roomB"] },
         { "id": "sensor2", "rooms": ["roomB", "roomC"] },
      ],
      "source_sensor": "roomA",
      "target_sensor": "roomC"
    }
    """

    room_mapping = Room.create_room_mapping_from_schemas(request_body.rooms)

    sensors = Sensor.create_sensors_from_schemas(request_body.sensors, room_mapping)

    sensor_graph = SensorGraph(sensors)
    sensor_graph.build_graph()

    # 4. Optionally compute the fastest path if source/target are provided.
    path, distance = None, None
    if request_body.source_sensor and request_body.target_sensor:
        path, distance = sensor_graph.find_fastest_path(
            source=request_body.source_sensor,
            target=request_body.target_sensor
        )

    # Example call to your existing service, if it’s still relevant:
    # create_fastest_path({})

    return {
        "fastest_path": path,
        "distance": distance
    }