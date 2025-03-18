from db.database import Database
from db.models.room import Room

# Initialize database connection
db = Database()

# Create and save a new room
room = Room(
    name="please my god",
    type="LOBBY",
    crowd_factor=0.3,
    area=120.0,
    longitude=100,
    latitude=100
).save()

# Verify data was persisted
all_rooms = Room.objects()
# Print rooms with their details
for room in all_rooms:
    print(f"Room: {room.name} (Type: {room.type}, Area: {room.area}m², Crowd Factor: {room.crowd_factor})")
