class Sensor:
    def __init__(self, id, room_ids):
        self.id = id
        self.room_ids = room_ids  # List of room IDs (as provided by the API)
        self.rooms = []  # This will later hold full Room objects

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            room_ids=data.get("rooms", [])
        )

    def attach_rooms(self, room_mapping: dict):
        """
        Replace room_ids with full Room objects using a room mapping.
        """
        self.rooms = [room_mapping[room_id] for room_id in self.room_ids if room_id in room_mapping]