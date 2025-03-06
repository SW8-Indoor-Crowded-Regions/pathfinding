import datetime
from models import Database, rooms_validator, sensors_validator, visitors_validator

# Connect to database
db = Database()

# Example: Insert a room
room = db.rooms.insert_one({
    "name": "Conference Room",
    "type": "MEETING",
    "crowdFactor": 0.8,
    "area": 45.5
})

# Example: Query rooms
all_rooms = list(db.rooms.find())

print(all_rooms)
# Example: Insert a sensor for the room
sensor = db.sensors.insert_one({
    "name": "Sensor-LOL",
    "movements": [[5, 3], [1, 2]],
    "roomId": room.inserted_id
})

# Example: Insert a visitor
visitor = db.visitors.insert_one({
    "name": "John Doe",
    "visitedRooms": [room.inserted_id],
    "visitDate": datetime.datetime.now()
})

# Don't forget to close the connection when done
db.close()