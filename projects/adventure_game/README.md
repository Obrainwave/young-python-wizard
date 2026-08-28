# Text-Based Adventure Game

A command-line adventure game where you explore a mysterious mansion, solve a puzzle, and find the Crown of Wisdom. Built with Python and SQLite, this project demonstrates clean object-oriented architecture with separated models, services, and storage layers.

This project is part of the **Young Python Wizard** series and is designed to teach how to build interactive, production-ready applications.

---

## Game Overview

**Story:** You wake up in an old mansion. Your mission is to find the **Rusty Key**, unlock the **Storage Room**, and retrieve the **Crown of Wisdom** to win the game.

**Objective:** Explore rooms, collect items, solve a simple puzzle, and reach the Treasure Room with the Crown.

---

## Features

- 🏰 Explore 5 interconnected rooms with descriptive text.
- 🔑 Pick up and use items (e.g., use the Rusty Key to unlock a door).
- 💡 Get contextual hints when stuck.
- 💾 Save and load game progress (current room, inventory, and flags).
- 🎯 Clear win condition with congratulatory message.
- 🗄️ Persistent storage using SQLite.
- 📖 Built-in how-to-play instructions.

---

## Commands

| Command          | Description                              |
|------------------|------------------------------------------|
| `look`           | Describe current room                    |
| `go [direction]` | Move (north, south, east, west)          |
| `take [item]`    | Pick up an item                          |
| `use [item]`     | Use an item from inventory               |
| `inventory`      | Show items you carry                     |
| `hint`           | Get a contextual hint                    |
| `help`           | Show all commands                        |
| `save`           | Save game progress                       |
| `quit`           | Quit (saves automatically)               |

---

## Project Structure

```
adventure_game/
├── models/
│   ├── __init__.py
│   ├── room.py
│   ├── item.py
│   └── player_state.py
├── services/
│   ├── __init__.py
│   └── game_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── room_repository.py
│   ├── item_repository.py
│   └── player_state_repository.py
├── data/
│   └── seed_game.py
└── main.py
```

- **`models/`** – Data classes (`Room`, `Item`, `PlayerState`).
- **`services/`** – Game logic (`GameService` handles commands, movement, puzzle, hints).
- **`storage/`** – Database connection, initialization, and repositories.
- **`data/seed_game.py`** – Script to populate the game world with rooms and items.
- **`main.py`** – Command-line interface and game loop.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses only the standard library)

### Installation

1. Clone or download this repository.
2. Navigate to the `adventure_game` folder.

### Setting Up the Game World

Before playing for the first time, seed the database:

```bash
python data/seed_game.py
```

This creates rooms, links them, and places items.

### Running the Game

```bash
python main.py
```

The game will load your saved progress or start a new game.

---

## How to Play

1. You start in the **Entrance Hall**.
2. Type `go north` to enter the **Library**.
3. Type `take rusty key` to pick up the key.
4. Type `go south` to return, then `go east` to the **Dining Room**, then `go north` to the **Kitchen**.
5. In the Kitchen, the east door is locked. Type `use rusty key` to unlock it.
6. Type `go east` to enter the **Storage Room**.
7. Type `take crown` to win!

Use `hint` if you're stuck.

---

## How It Works

### Database Initialization

`DatabaseInitializer` creates three tables (`rooms`, `items`, `player_state`) if they don't already exist.

### Game World Seeding

`data/seed_game.py` inserts rooms with descriptions and exits, creates items, and links rooms together. It also sets up the locked door puzzle.

### Game Logic

- `GameService` manages the current `PlayerState` (room, inventory, flags).
- Movement checks for locked doors (e.g., east from Kitchen requires `unlock_east_door` flag).
- Items can be taken (moved from room to inventory) and used (set flags).
- Hints are contextual: based on current room and inventory.
- Win condition: player is in Storage Room and has the Crown.

### Persistence

- Player progress is saved to SQLite as a singleton row (`id=1`).
- Inventory and flags are stored as JSON strings.

---

## Extending the Project

Here are some ideas to enhance the game:

- Add more rooms and items.
- Implement multiple puzzles and endings.
- Add a `drop` command.
- Introduce NPCs or enemies.
- Create a simple GUI using Tkinter.
- Write unit tests for the service layer.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy adventuring! 🗡️🐍