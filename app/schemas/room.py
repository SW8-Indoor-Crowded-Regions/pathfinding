from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class RoomSchema(BaseModel):
    id: UUID = Field(..., description="Unique identifier for the room.")
    name: Optional[str] = Field(..., description="Name of the room.")
    crowd_factor: int = Field(..., description="Crowd factor of the room.")
