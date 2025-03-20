from pydantic import BaseModel
from typing import List
from room import RoomSchema
from sensor import SensorSchema

class FastestPathRequest(BaseModel):
    rooms: List[RoomSchema]
    sensors: List[SensorSchema]
    source_sensor: str
    target_sensor: str