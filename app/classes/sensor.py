class Sensor:
	def __init__(
		self,
		id: str,
		longitude: float,
		latitude: float,
		is_vertical: bool,
		rooms: list | None = None,
	):
		"""
		Initializes a Sensor object.

		Args:
		    id (str): The unique identifier for the sensor.
		    longitude (float): The longitude coordinate of the sensor.
		    latitude (float): The latitude coordinate of the sensor.
		    rooms (list, optional): A list of Room objects associated with this sensor.
		                             Defaults to an empty list if None.
		"""
		self.id = id
		self.longitude = longitude
		self.latitude = latitude
		self.rooms = rooms if rooms is not None else []
		self.is_vertical = is_vertical

	@classmethod
	def from_schema(cls, schema, room_mapping: dict):
		"""
		Creates a Sensor instance from a schema object and a room mapping.

		Args:
		    schema: An object with attributes 'id', 'longitude', 'latitude', 'rooms' (list of room IDs).
		    room_mapping (dict): A dictionary mapping room IDs to Room objects.

		Returns:
		    Sensor: A new Sensor instance with associated Room objects populated.
		"""
		room_ids = schema.rooms if hasattr(schema, 'rooms') else []
		associated_rooms = [
			room_mapping[room_id] for room_id in room_ids if room_id in room_mapping
		]

		sensor = cls(
			id=schema.id,
			longitude=schema.longitude,
			latitude=schema.latitude,
			rooms=associated_rooms,
			is_vertical=schema.is_vertical,
		)
		return sensor

	@classmethod
	def create_sensors_from_schemas(cls, sensor_schemas: list, room_mapping: dict):
		"""
		Creates a list of Sensor objects from a list of schemas and a room mapping.

		Args:
		    sensor_schemas (list): A list of schema objects for sensors.
		    room_mapping (dict): A dictionary mapping room IDs to Room objects.

		Returns:
		    list[Sensor]: A list of fully initialized Sensor objects.
		"""
		sensors = []
		for schema in sensor_schemas:
			sensor = cls.from_schema(schema, room_mapping)
			sensors.append(sensor)

		return sensors

	def __repr__(self):
		room_ids_repr = [room.id for room in self.rooms]
		return f"Sensor(id='{self.id}', rooms={room_ids_repr}, lon={self.longitude}, lat={self.latitude})"
