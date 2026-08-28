import os
import sys

# Get the path of the current script's folder
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the path of the parent folder (stepping out once)
parent_dir = os.path.dirname(current_dir)

# Add the parent folder to sys.path
sys.path.append(parent_dir)

from storage.database import Database
from storage.initializer import DatabaseInitializer
from storage.room_repository import RoomRepository
from storage.item_repository import ItemRepository
from models.room import Room
from models.item import Item

def seed():
    db = Database("adventure.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    room_repo = RoomRepository(db)
    item_repo = ItemRepository(db)

    # Create rooms
    entrance = room_repo.insert(Room(
        name="Entrance Hall",
        description="A dusty hall with doors to the north and east."
    ))
    library = room_repo.insert(Room(
        name="Library",
        description="Shelves of old books line the walls. A key lies on a table."
    ))
    kitchen = room_repo.insert(Room(
        name="Kitchen",
        description="A cold fireplace and a wooden table. There's a locked door to the east."
    ))
    treasure_room = room_repo.insert(Room(
        name="Treasure Room",
        description="Glittering gold and jewels! You won the game!"
    ))

    # Link rooms
    entrance.north = library.id
    entrance.east = kitchen.id
    library.south = entrance.id
    kitchen.west = entrance.id
    kitchen.east = treasure_room.id   # locked door
    treasure_room.west = kitchen.id

    # Update rooms with links
    room_repo.update(entrance)
    room_repo.update(library)
    room_repo.update(kitchen)
    room_repo.update(treasure_room)

    # Create items
    key = item_repo.insert(Item(
        name="key",
        description="A rusty iron key.",
        room_id=entrance.id,
        is_usable=True,
        effect="door_unlocked"
    ))
    book = item_repo.insert(Item(
        name="book",
        description="An old, dusty tome.",
        room_id=library.id,
        is_usable=False
    ))
    sword = item_repo.insert(Item(
        name="sword",
        description="A shiny blade.",
        room_id=kitchen.id,
        is_usable=False
    ))

    print("Game world seeded with rooms and items.")
    items = item_repo.get_all_items()
    print(f"DEBUG: All items in database: {[item.name for item in items]}")
    db.close()

if __name__ == "__main__":
    seed()