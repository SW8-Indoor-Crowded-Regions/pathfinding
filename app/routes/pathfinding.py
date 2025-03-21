from fastapi import APIRouter, HTTPException
from ..services.route_service import create_fastest_path
from ..schemas.path import FastestPathRequest

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
        return create_fastest_path(request_body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
