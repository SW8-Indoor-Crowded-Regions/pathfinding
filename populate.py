from db.models.room import Room
from db.models.sensor import Sensor
from db.database import Database

db = Database()

# Example adjacency (doors/openings) for the middle rooms from the floor plan.
# Extend as needed for the rest of the rooms on your floor plan.
ROOM_ADJACENCY = {
    "201A": ["201B", "211B", "202", "P1"],
    "201B": ["201A", "201C"],
    "201C": ["201B", "201D"],
    "201D": ["201E", "209"],
    "201E": ["201D", "204"],
    "202": ["203", "201A"],
    "203": ["202", "204"],
    "204": ["203", "201E"],
    "211B": ["201A", "211A"],
    "211A": ["211B", "210B"],
    "210B": ["211A", "210A"],
    "210A": ["209", "210B"],
    "208B": ["209", "208A", "205"],
    "208A": ["208B", "207"],
    "207": ["208A", "206"],
    "206": ["207", "205"],
    "205": ["206", "204", "208B", "208A"],
    "P1": ["201A", "202", "212", "P2", "P3"],
    "209": ["210A", "201D"],
    "209": ["210A", "201D"],
    "209": ["210A", "201D"],
    "209": ["210A", "201D"],
    "209": ["210A", "201D"],
    "209": ["210A", "201D"],
    "209": ["210A", "201D"],
    "209": ["210A", "201D"],
    "209": ["210A", "201D"],
    "209": ["210A", "201D"],

}

def create_rooms_and_sensors():
    """
    Creates Room documents for each labeled room in ROOM_ADJACENCY,
    and creates Sensor documents for each doorway/opening between rooms.
    """

    # Dictionary to store {room_name: Room_object} after creation
    room_objects = {}

    # 1) Create Room objects in the database
    for room_name in ROOM_ADJACENCY.keys():
        # Example dummy data - adjust as needed
        room = Room(
            name=room_name,
            type="EXHIBITION",      # or LOBBY, OFFICE, etc.
            crowd_factor=0.3,      # dummy crowd factor
            area=50.0,             # dummy area
            longitude=0.0,         # dummy coordinates
            latitude=0.0
        ).save()

        room_objects[room_name] = room

    # 2) Create Sensor objects for each pair of adjacent rooms
    #    We'll keep track of pairs we've already processed to avoid duplicates.
    created_pairs = set()
    for room_name, neighbors in ROOM_ADJACENCY.items():
        for neighbor_name in neighbors:
            # Sort the pair so (201B, 201C) is the same as (201C, 201B)
            pair = tuple(sorted([room_name, neighbor_name]))

            if pair not in created_pairs:
                sensor_name = f"Sensor_{pair[0]}_{pair[1]}"
                sensor = Sensor(
                    name=sensor_name,
                    movements=[],  # or any data you have
                    rooms=[room_objects[pair[0]], room_objects[pair[1]]]
                )
                sensor.save()

                created_pairs.add(pair)

    print("Rooms and sensors created successfully!")

create_rooms_and_sensors()
