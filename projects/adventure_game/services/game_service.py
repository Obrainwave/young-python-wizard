from models.room import Room
from models.item import Item
from models.player_state import PlayerState
from storage.room_repository import RoomRepository
from storage.item_repository import ItemRepository
from storage.player_state_repository import PlayerStateRepository

class GameService:
    def __init__(self, db):
        self.room_repo = RoomRepository(db)
        self.item_repo = ItemRepository(db)
        self.state_repo = PlayerStateRepository(db)
        self.current_state = None
        self.running = False

    def new_game(self):
        """Start a new game from the first room (id=1)."""
        first_room = self.room_repo.get_by_id(1)
        if not first_room:
            raise ValueError("No rooms defined. Please seed the database.")
        self.current_state = PlayerState(current_room_id=first_room.id)
        self.state_repo.save(self.current_state)
        self.running = True

    def load_game(self):
        """Load saved game state."""
        state = self.state_repo.load()
        if state:
            self.current_state = state
            self.running = True
            return True
        return False

    def save_game(self):
        if self.current_state:
            self.state_repo.save(self.current_state)

    def get_current_room(self):
        if not self.current_state:
            return None
        return self.room_repo.get_by_id(self.current_state.current_room_id)

    def get_items_in_room(self, room_id):
        items = self.item_repo.get_all_items()
        return self.item_repo.get_by_room(room_id)

    def get_inventory_items(self):
        """Return list of Item objects for inventory IDs."""
        items = []
        for item_id in self.current_state.inventory:
            item = self.item_repo.get_by_id(item_id)
            if item:
                items.append(item)
        return items

    def move(self, direction):
        room = self.get_current_room()
        if not room:
            return False
        dest_id = getattr(room, direction)
        if dest_id:
            # Check for locked door (east from Kitchen to Treasure Room)
            if room.name == "Kitchen" and direction == "east":
                if not self.current_state.flags.get("door_unlocked", False):
                    return False  # can't move, door is locked
            self.current_state.current_room_id = dest_id
            self.save_game()
            return True
        return False

    def take_item(self, item_name):
        """Pick up an item from the current room. Returns (success, message)."""
        room = self.get_current_room()
        if not room:
            return False, "You are nowhere."
        items_in_room = self.get_items_in_room(room.id)
        for item in items_in_room:
            if item.name.lower() == item_name.lower():
                if item.id in self.current_state.inventory:
                    return False, f"You already have {item.name}."
                self.current_state.inventory.append(item.id)
                self.item_repo.update_room(item.id, None)
                self.save_game()
                return True, f"You picked up {item.name}."
        return False, f"There is no {item_name} here."

    def use_item(self, item_name):
        """Use an item from inventory. Returns (success, message)."""
        for item_id in self.current_state.inventory:
            item = self.item_repo.get_by_id(item_id)
            if item and item.name.lower() == item_name.lower():
                if item.is_usable:
                    if item.effect:
                        self.current_state.flags[item.effect] = True
                        self.save_game()
                        return True, f"You use {item.name}. {item.effect} happens!"
                    else:
                        return True, f"You use {item.name}. Nothing happens."
                else:
                    return False, f"{item.name} cannot be used."
        return False, f"You don't have {item_name}."

    def look(self):
        """Return description of current room and visible items."""
        room = self.get_current_room()
        if not room:
            return "You are in a void."
        text = f"**{room.name}**\n{room.description}\n"
        items = self.get_items_in_room(room.id)
        if items:
            text += "\nYou see: " + ", ".join(i.name for i in items)
        else:
            text += "\nThere are no items here."
        return text

    def quit(self):
        self.running = False
        self.save_game()