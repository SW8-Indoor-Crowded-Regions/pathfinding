class Sensor:
    def __init__(self, id: str, room_ids: list):
        self.id = id
        self.room_ids = room_ids  # List of room IDs (as provided by the API)
        self.rooms = []  # This will later hold full Room objects

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            room_ids=data.get("rooms", [])
        )

    @classmethod
    def from_schema(cls, schema):
        """
        Factory that creates a Sensor from a Pydantic schema instance
        (for example, SensorSchema).
        """
        return cls(
            id=schema.id,
            room_ids=schema.rooms
        )

    @classmethod
    def create_sensors_from_schemas(cls, sensor_schemas: list, room_mapping: dict):
        """
        Convenience method that takes a list of sensor schemas,
        attaches Rooms to them, and returns a list of Sensor objects.
        """
        sensors = []
        for schema in sensor_schemas:
            sensor = cls.from_schema(schema)
            sensor.attach_rooms(room_mapping)
            sensors.append(sensor)
        return sensors

    def attach_rooms(self, room_mapping: dict):
        """
        Replace room_ids with full Room objects using a room mapping.
        """
        self.rooms = [
            room_mapping[room_id]
            for room_id in self.room_ids
            if room_id in room_mapping
        ]
