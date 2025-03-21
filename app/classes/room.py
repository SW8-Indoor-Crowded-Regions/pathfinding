class Room:
    def __init__(self, id: str, name: str, crowd_factor: float):
        self.id = id
        self.name = name
        self.crowd_factor = crowd_factor

    @classmethod
    def from_dict(cls, data: dict):
        return cls(id=data.get('id'), name=data.get('name'), crowd_factor=data.get('crowd_factor'))

    @classmethod
    def from_schema(cls, schema):
        """
        Factory that creates a Room from a Pydantic schema instance
        (for example, RoomSchema).
        """
        return cls(id=schema.id, name=schema.name, crowd_factor=schema.crowd_factor)

    @classmethod
    def create_room_mapping_from_schemas(cls, room_schemas: list):
        """
        Convenience method that takes a list of room schemas
        and returns a dictionary {room_id: Room instance}.
        """
        room_mapping = {}
        for schema in room_schemas:
            room_obj = cls.from_schema(schema)
            room_mapping[room_obj.id] = room_obj
        return room_mapping
