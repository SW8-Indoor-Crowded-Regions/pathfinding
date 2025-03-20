from fastapi import APIRouter
from ..services.route_service import create_fastest_path

router = APIRouter(prefix="/pathfinding")

@router.get("/fastest-path")
async def get_fastest_path():
    path = create_fastest_path({})
    return {"message": path}
