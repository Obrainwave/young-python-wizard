class Room:
    def __init__(self, room_id=None, name="", description="", north=None, south=None, east=None, west=None):
        self.id = room_id
        self.name = name
        self.description = description
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    def __repr__(self):
        return f"Room(id={self.id}, name='{self.name}')"