from fastapi import APIRouter
from ..services.route_service import create_least_crowded_path

router = APIRouter(prefix="/pathfinding")

@router.get("/least-crowded-path")
async def get_least_crowded_path():
    path = create_least_crowded_path({})
    return {"message": path}
