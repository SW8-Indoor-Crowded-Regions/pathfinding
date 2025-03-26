from pydantic import BaseModel, Field
from typing import Optional


class RoomSchema(BaseModel):
    id: str = Field(..., description="Unique identifier for the room.")
    name: Optional[str] = Field(..., description="Name of the room.")
    occupants: int = Field(..., description="Number of occupants in the room.")
    area: float = Field(..., description="Area of the room in square meters.")
    crowd_factor: float = Field(..., description="Crowd factor of the room.")
