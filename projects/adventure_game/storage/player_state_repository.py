import json
from models.player_state import PlayerState

class PlayerStateRepository:
    def __init__(self, db):
        self.db = db

    def save(self, state):
        """Insert or update the singleton player state."""
        # Check if exists
        self.db.execute("SELECT id FROM player_state WHERE id = 1")
        row = self.db.fetchone()
        if row:
            self.db.execute(
                "UPDATE player_state SET current_room_id = ?, inventory = ?, flags = ? WHERE id = 1",
                (state.current_room_id, json.dumps(state.inventory), json.dumps(state.flags))
            )
        else:
            self.db.execute(
                "INSERT INTO player_state (id, current_room_id, inventory, flags) VALUES (1, ?, ?, ?)",
                (state.current_room_id, json.dumps(state.inventory), json.dumps(state.flags))
            )
        self.db.commit()

    def load(self):
        self.db.execute("SELECT * FROM player_state WHERE id = 1")
        row = self.db.fetchone()
        if row:
            return PlayerState(
                id=row["id"],
                current_room_id=row["current_room_id"],
                inventory=json.loads(row["inventory"]) if row["inventory"] else [],
                flags=json.loads(row["flags"]) if row["flags"] else {}
            )
        return None