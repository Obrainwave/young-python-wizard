import json

class DatabaseInitializer:
    def __init__(self, db):
        self.db = db

    def initialize(self):
        """Create tables only if they don't already exist."""
        required_tables = ["rooms", "items", "player_state"]
        all_exist = all(self.db.table_exists(t) for t in required_tables)

        if all_exist:
            return

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                north INTEGER,
                south INTEGER,
                east INTEGER,
                west INTEGER,
                FOREIGN KEY (north) REFERENCES rooms(id),
                FOREIGN KEY (south) REFERENCES rooms(id),
                FOREIGN KEY (east) REFERENCES rooms(id),
                FOREIGN KEY (west) REFERENCES rooms(id)
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                room_id INTEGER,
                is_usable INTEGER DEFAULT 0,
                effect TEXT,
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS player_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                current_room_id INTEGER,
                inventory TEXT,
                flags TEXT,
                FOREIGN KEY (current_room_id) REFERENCES rooms(id)
            )
        """)
        self.db.commit()
        print("Database initialized.")