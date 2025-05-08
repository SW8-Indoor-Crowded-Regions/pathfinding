from pydantic import BaseModel, Field
from typing import List


class SensorSchema(BaseModel):
	id: str = Field(..., description='Unique identifier for the sensor.')
	rooms: List[str] = Field(..., description='List of room UUIDs associated with the sensor.')
	longitude: float = Field(..., description="Longitude of the sensor's location.")
	latitude: float = Field(..., description="Latitude of the sensor's location.")
	is_vertical: bool = Field(
		..., description='Indicates if the sensor is vertical (True) or horizontal (False).'
	)
