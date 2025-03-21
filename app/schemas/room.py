from pydantic import BaseModel
from typing import Optional


class RoomSchema(BaseModel):
    id: str
    name: Optional[str] = None
    crowd_factor: float
