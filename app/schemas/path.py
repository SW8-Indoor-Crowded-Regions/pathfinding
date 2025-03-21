from pydantic import BaseModel
from typing import List, Optional
from .room import RoomSchema
from .sensor import SensorSchema

class FastestPathRequest(BaseModel):
    rooms: Optional[List[RoomSchema]] = None
    sensors: Optional[List[SensorSchema]] = None
    source_sensor: str
    target_sensor: str