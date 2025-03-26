from pydantic import BaseModel, Field
from typing import List
from .room import RoomSchema
from .sensor import SensorSchema


class FastestPathRequest(BaseModel):
    rooms: List[RoomSchema] = Field(description="List of rooms involved in pathfinding.")
    sensors: List[SensorSchema] = Field(description="List of sensors involved in pathfinding.")
    source_sensor: str = Field(..., description="ID of the source sensor.")
    target_sensor: str = Field(..., description="ID of the target sensor.")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "rooms": [
                    {"id": "123e4567-e89b-12d3-a456-426614174000", "name": "Lobby", "crowd_factor": 2, "occupants": 10, "area": 100},
                    {"id": "123e4567-e89b-12d3-a456-426614174001", "name": "Hallway", "crowd_factor": 1, "occupants": 5, "area": 50},
                    {"id": "123e4567-e89b-12d3-a456-426614174002", "name": "Meeting Room", "crowd_factor": 3, "occupants": 20, "area": 200}
                ],
                "sensors": [
                    {"id": "sensor1", "rooms": ["123e4567-e89b-12d3-a456-426614174000", "123e4567-e89b-12d3-a456-426614174001"]},
                    {"id": "sensor2", "rooms": ["123e4567-e89b-12d3-a456-426614174001", "123e4567-e89b-12d3-a456-426614174002"]}
                ],
                "source_sensor": "sensor1",
                "target_sensor": "sensor2"
            }
        }
