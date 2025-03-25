from pydantic import BaseModel, Field
from typing import List


class SensorSchema(BaseModel):
    id: str = Field(..., description="Unique identifier for the sensor.")
    rooms: List[str] = Field(..., description="List of room UUIDs associated with the sensor.")

