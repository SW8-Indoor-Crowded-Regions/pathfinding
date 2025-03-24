from app.classes.room import Room


class TestRoom:
    def test_from_dict(self):
        data = {'id': 'room1', 'name': 'Main Hall', 'crowd_factor': 10, 'occupants': 100, 'area': 200}
        room = Room.from_dict(data)
        assert room.id == 'room1'
        assert room.name == 'Main Hall'
        assert room.crowd_factor == 10
