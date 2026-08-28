from models.room import Room

class RoomRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, room):
        self.db.execute(
            "INSERT INTO rooms (name, description, north, south, east, west) VALUES (?, ?, ?, ?, ?, ?)",
            (room.name, room.description, room.north, room.south, room.east, room.west)
        )
        self.db.commit()
        room.id = self.db.last_row_id()
        return room

    def get_by_id(self, room_id):
        self.db.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
        row = self.db.fetchone()
        if row:
            return self._row_to_room(row)
        return None

    def get_all(self):
        self.db.execute("SELECT * FROM rooms")
        rows = self.db.fetchall()
        return [self._row_to_room(row) for row in rows]
    
    def update(self, room):
        self.db.execute(
            "UPDATE rooms SET name = ?, description = ?, north = ?, south = ?, east = ?, west = ? WHERE id = ?",
            (room.name, room.description, room.north, room.south, room.east, room.west, room.id)
        )
        self.db.commit()

    def _row_to_room(self, row):
        return Room(
            room_id=row["id"],
            name=row["name"],
            description=row["description"],
            north=row["north"],
            south=row["south"],
            east=row["east"],
            west=row["west"]
        )