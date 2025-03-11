from db.models.room import Room
from db.models.sensor import Sensor
from db.database import Database

db = Database()

# Example adjacency (doors/openings) for the middle rooms from the floor plan.
# Extend as needed for the rest of the rooms on your floor plan.
ROOM_ADJACENCY = {
    # -- Ring wing --
    "201A": ["201B", "211B", "202", "P1"],
    "201B": ["201A", "201C"],
    "201C": ["201B", "201D"],
    "201D": ["201E", "209"],
    "201E": ["201D", "204"],
    "202": ["203", "201A", "P1"],
    "203": ["202", "204"],
    "204": ["203", "201E", "205"],
    "211B": ["201A", "211A"],
    "211A": ["211B", "210B"],
    "210B": ["211A", "210A"],
    "210A": ["209", "210B"],
    "208B": ["209", "208A", "205"],
    "209": ["210A", "208B", "201D"],
    "208A": ["208B", "207"],
    "207": ["208A", "206"],
    "206": ["207", "205"],
    "205": ["206", "204", "208B", "208A"],

    # -- middle passage etc --
    "P1": ["201A", "202", "212", "P2", "P3"],
    "P2": ["P1", "P4"],
    "P3": ["P1", "P4"],
    "P4": ["P3", "P2", "229", "217A", "216"],
    "212": ["P1", "213"],
    "213": ["212", "214"],
    "214": ["213", "215"],
    "215": ["214", "216"],
    "216": ["P4", "215"],

    # -- left wing --
    "217A": ["218A", "229", "217B", "P4"],
    "229": ["217A", "P4", "228"],
    "228": ["229", "227"],
    "227": ["228", "217F", "221"],
    "217F": ["217E", "220", "227"],
    "217E": ["217F", "217D"],
    "217D": ["217E", "217C"],
    "217C": ["217D", "217B"],
    "217B": ["217C", "217A"],
    "218A": ["218B", "217A"],
    "218B": ["218A", "219"],
    "219": ["218B", "220"],
    "220": ["219", "217F", "P7"],
    "P7": ["220", "221", "222"],
    "222": ["P7", "223"],
    "223": ["221", "222", "224"],
    "224": ["223", "225"],
    "225": ["226", "221", "224"],
    "221": ["P7", "225", "223", "227"],
    "226": ["225"],

    # -- left new building --
    "P5": ["218A", "P8", "P9"],
    "P8": ["270B", "270A", "262", "272", "261", "P5"],
    "270B": ["P8"],
    "270A": ["P8"],
    "262": ["P8", "261"],
    "261": ["P8", "262"],
    "272": ["P8", "260"],
    "260": ["272"],

    # -- middle new building --
    "P9": ["269A", "269B", "263B", "263C", "P6", "P5"],
    "269A": ["P9"],
    "269B": ["P9"],
    "263B": ["263C", "P9"],
    "263C": ["P9", "263B", "263A"],
    "263A": ["263C"],

    # -- right new building
    "P6": ["P9", "P10", "211B"],
    "P10": ["P6", "268A", "268B", "264", "267", "265", "266"],
    "268A": ["P10"],
    "268B": ["P10"],
    "264": ["P10", "264A"],
    "264A": ["264"],
    "267": ["P10"],
    "265": ["P10", "266"],
    "266": ["P10", "265"],
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
