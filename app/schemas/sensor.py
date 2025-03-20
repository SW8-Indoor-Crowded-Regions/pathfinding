from pydantic import BaseModel
from typing import List

class SensorSchema(BaseModel):
    id: str
    rooms: List[str]