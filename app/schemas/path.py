from pydantic import BaseModel, Field
from typing import List
from .room import RoomSchema
from .sensor import SensorSchema


class FastestPathRequest(BaseModel):
	rooms: List[RoomSchema] = Field(description='List of rooms involved in pathfinding.')
	sensors: List[SensorSchema] = Field(description='List of sensors involved in pathfinding.')
	source_room: str = Field(..., description='ID of the source room.')
	target_room: str = Field(..., description='ID of the target room.')

	class ConfigDict:
		json_schema_extra = {
			'example': {
				'rooms': [
					{
						'id': 'room1',
						'name': 'Lobby',
						'crowd_factor': 2,
						'occupants': 10,
						'area': 100,
					},
					{
						'id': 'room2',
						'name': 'Hallway',
						'crowd_factor': 1,
						'occupants': 5,
						'area': 50,
					},
					{
						'id': 'room3',
						'name': 'Meeting Room',
						'crowd_factor': 3,
						'occupants': 20,
						'area': 200,
					},
				],
				'sensors': [
					{'id': 'sensor1', 'rooms': ['room1', 'room2']},
					{'id': 'sensor2', 'rooms': ['room2', 'room3']},
				],
				'source_room': 'room2',
				'target_room': 'room2',
			}
		}


class MultiplePointsRequest(BaseModel):
	rooms: List[RoomSchema] = Field(description='List of rooms involved in pathfinding.')
	sensors: List[SensorSchema] = Field(description='List of sensors involved in pathfinding.')
	source_room: str = Field(..., description='ID of the source room.')
	target_rooms: List[str] = Field(..., description='List of target room IDs.')

	class ConfigDict:
		json_schema_extra = {
			'example': {
				'rooms': [
					{
						'id': 'room1',
						'name': 'Lobby',
						'crowd_factor': 2,
						'occupants': 10,
						'area': 100,
					},
					{
						'id': 'room2',
						'name': 'Hallway',
						'crowd_factor': 1,
						'occupants': 5,
						'area': 50,
					},
					{
						'id': 'room3',
						'name': 'Meeting Room',
						'crowd_factor': 3,
						'occupants': 20,
						'area': 200,
					},
				],
				'sensors': [
					{'id': 'sensor1', 'rooms': ['room1', 'room2']},
					{'id': 'sensor2', 'rooms': ['room2', 'room3']},
				],
				'source_room': 'room2',
				'target_rooms': ['room1', 'room3'],
			}
		}