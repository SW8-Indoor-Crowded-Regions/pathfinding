import os
from fastapi import APIRouter
from ..services.route_service import create_fastest_path
from ..schemas.path import FastestPathRequest
from ..classes.room import Room
from ..classes.sensor import Sensor
from ..classes.sensor_graph import SensorGraph

router = APIRouter(prefix="/pathfinding")

@router.post("/fastest-path")
async def get_fastest_path(request_body: FastestPathRequest):
    """
    Accepts a JSON payload that contains optional lists of Rooms and Sensors,
    as well as source and target sensors for pathfinding.

    Example of request_body:
    {
      "rooms": [
         { "id": "UUID1", "name": "Lobby", "crowd_factor": 2 },
         { "id": "UUID2", "name": "Hallway", "crowd_factor": 1 },
         { "id": "UUID3", "name": "Meeting Room", "crowd_factor": 3 }
      ],
      "sensors": [
         { "id": "sensor1", "rooms": ["UUID1", "UUID2"] },
         { "id": "sensor2", "rooms": ["UUID2", "UUID3"] }
      ],
      "source_sensor": "sensor1",
      "target_sensor": "sensor2"
    }
    """

    try:
        rooms = Room.create_room_mapping_from_schemas(request_body.rooms or [])
        sensors = Sensor.create_sensors_from_schemas(request_body.sensors or [], rooms)

        source_sensor = request_body.source_sensor
        target_sensor = request_body.target_sensor

        graph_filename = r"C:\Github\SW8\pathfinding\app\sensor_graph.pickle"

        sensor_graph = SensorGraph(sensors)
        if os.path.exists(graph_filename):
            try:
                print(f"load graph")
                sensor_graph.load_graph(graph_filename)
            except Exception as e:
                print(f"build graph")
                sensor_graph.build_graph()
                sensor_graph.save_graph(graph_filename)
        else:
            print(f"build graph without loading")
            sensor_graph.build_graph()
            sensor_graph.save_graph(graph_filename)

        path, distance = sensor_graph.find_fastest_path(source_sensor, target_sensor)

        if not path or not distance:
            return {
                "error": "No path found."
            }
        return {
            "fastest_path": path,
            "distance": distance
        }

    except Exception as e:
        return {
            "error": str(e)
        }
