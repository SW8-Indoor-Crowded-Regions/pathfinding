from fastapi import APIRouter, HTTPException
from ..controllers.route_service import create_fastest_path
from ..schemas.path import FastestPathRequest

router = APIRouter(prefix='/pathfinding')


@router.post('/fastest-path')
async def get_fastest_path(request_body: FastestPathRequest):
    """
    Calculate the fastest path based on the provided rooms and sensors.

    - **rooms**: List of rooms with their unique IDs, names, and crowd factors.
    - **sensors**: List of sensors with their unique IDs and associated room IDs.
    - **source_room**: ID of the source room.
    - **target_room**: ID of the target room.
    """
    try:
        return create_fastest_path(request_body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error: ' + str(e))
