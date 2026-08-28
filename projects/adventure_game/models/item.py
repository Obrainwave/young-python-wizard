class Item:
    def __init__(self, item_id=None, name="", description="", room_id=None, is_usable=False, effect=""):
        self.id = item_id
        self.name = name
        self.description = description
        self.room_id = room_id
        self.is_usable = is_usable
        self.effect = effect

    def __repr__(self):
        return f"Item(id={self.id}, name='{self.name}')"