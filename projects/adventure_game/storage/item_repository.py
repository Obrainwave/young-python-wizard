from models.item import Item

class ItemRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, item):
        self.db.execute(
            "INSERT INTO items (name, description, room_id, is_usable, effect) VALUES (?, ?, ?, ?, ?)",
            (item.name, item.description, item.room_id, 1 if item.is_usable else 0, item.effect)
        )
        self.db.commit()
        item.id = self.db.last_row_id()
        return item
    
    from models.item import Item

class ItemRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, item):
        self.db.execute(
            "INSERT INTO items (name, description, room_id, is_usable, effect) VALUES (?, ?, ?, ?, ?)",
            (item.name, item.description, item.room_id, 1 if item.is_usable else 0, item.effect)
        )
        self.db.commit()
        item.id = self.db.last_row_id()
        return item

    def get_by_id(self, item_id):
        self.db.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = self.db.fetchone()
        if row:
            return self._row_to_item(row)
        return None

    def get_by_room(self, room_id):
        self.db.execute("SELECT * FROM items WHERE room_id = ?", (room_id,))
        rows = self.db.fetchall()
        return [self._row_to_item(row) for row in rows]

    def update_room(self, item_id, room_id):
        """Set item's room_id (None means inventory)."""
        self.db.execute(
            "UPDATE items SET room_id = ? WHERE id = ?",
            (room_id, item_id)
        )
        self.db.commit()

    def get_all_items(self):
        self.db.execute("SELECT * FROM items")
        rows = self.db.fetchall()
        return [self._row_to_item(row) for row in rows]

    def get_by_id(self, item_id):
        self.db.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = self.db.fetchone()
        if row:
            return self._row_to_item(row)
        return None

    def get_by_room(self, room_id):
        self.db.execute("SELECT * FROM items WHERE room_id = ?", (room_id,))
        rows = self.db.fetchall()
        return [self._row_to_item(row) for row in rows]

    def update_room(self, item_id, room_id):
        """Set item's room_id (None means inventory)."""
        self.db.execute(
            "UPDATE items SET room_id = ? WHERE id = ?",
            (room_id, item_id)
        )
        self.db.commit()

    def _row_to_item(self, row):
        return Item(
            item_id=row["id"],
            name=row["name"],
            description=row["description"],
            room_id=row["room_id"],
            is_usable=bool(row["is_usable"]),
            effect=row["effect"]
        )