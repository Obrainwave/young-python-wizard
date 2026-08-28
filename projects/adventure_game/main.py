from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.game_service import GameService

def main():
    db = Database("adventure.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    service = GameService(db)

    # Attempt to load existing game; otherwise start new
    if not service.load_game():
        service.new_game()

    print("Welcome to the Adventure Game! Type 'help' for commands.")
    print("\n" + "="*50)
    print("HOW TO PLAY")
    print("="*50)
    print("Type commands to explore the world.")
    print("  look              - Describe current room")
    print("  go [direction]    - Move (north, south, east, west)")
    print("  take [item]       - Pick up an item")
    print("  use [item]        - Use an item (e.g., key)")
    print("  inventory         - Show your items")
    print("  save              - Save game")
    print("  quit              - Quit (saves automatically)")
    print("="*50 + "\n")
    
    print(service.look())

    while service.running:
        command = input("\n> ").strip().lower()
        if not command:
            continue
        parts = command.split()
        action = parts[0]
        if action == "help":
            print("Commands: look, go [direction], take [item], use [item], inventory, save, quit")
        elif action == "look":
            print(service.look())
        elif action == "go":
            if len(parts) < 2:
                print("Go where? (north, south, east, west)")
                continue
            direction = parts[1]
            if direction in ("north", "south", "east", "west", "n", "s", "e", "w"):
                if service.move(direction):
                    print(service.look())
                else:
                    print("You can't go that way.")
            else:
                print("Invalid direction.")
        elif action == "take":
            if len(parts) < 2:
                print("Take what?")
                continue
            item_name = " ".join(parts[1:])
            success, message = service.take_item(item_name)
            print(message)
        elif action == "use":
            if len(parts) < 2:
                print("Use what?")
                continue
            item_name = " ".join(parts[1:])
            success, message = service.use_item(item_name)
            print(message)
        elif action == "inventory":
            items = service.get_inventory_items()
            if items:
                print("Inventory: " + ", ".join(i.name for i in items))
            else:
                print("Your inventory is empty.")
        elif action == "save":
            service.save_game()
            print("Game saved.")
        elif action == "quit":
            print("Goodbye!")
            service.quit()
        else:
            print("Unknown command. Type 'help' for a list.")

    db.close()

if __name__ == "__main__":
    main()