class Room:
    def __init__(self, id, name, crowd_factor):
        self.id = id
        self.name = name
        self.crowd_factor = crowd_factor

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            crowd_factor=data.get("crowd_factor")
        )

