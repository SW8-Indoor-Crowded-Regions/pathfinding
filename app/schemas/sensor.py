from pydantic import BaseModel, Field
from typing import List
from uuid import UUID


class SensorSchema(BaseModel):
    id: str = Field(..., description="Unique identifier for the sensor.")
    rooms: List[UUID] = Field(..., description="List of room UUIDs associated with the sensor.")

