class PlayerState:
    def __init__(self, id=1, current_room_id=None, inventory=None, flags=None):
        self.id = id
        self.current_room_id = current_room_id
        self.inventory = inventory if inventory is not None else []
        self.flags = flags if flags is not None else {}

    def __repr__(self):
        return f"PlayerState(id={self.id}, room={self.current_room_id}, inventory={self.inventory})"