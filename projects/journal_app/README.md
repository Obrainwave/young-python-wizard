# File-Based Journal App

A command-line application for writing and managing personal journal entries. It uses a JSON file for persistent storage, so no database is required. The app supports creating, viewing, searching, editing, and deleting entries, with optional tags. Built with Python and object-oriented design, this project demonstrates clean separation of models, services, and storage layers.

This project is part of the **Young Python Wizard** series and is designed to teach how to build maintainable, production-ready applications using file-based storage.

---

## Features

- 📝 Create journal entries with title, content, and optional tags.
- 🔍 View all entries or a single entry by ID.
- 🔎 Search entries by title, content, or tags (case-insensitive).
- ✏️ Edit existing entries (only provided fields are changed).
- 🗑️ Delete entries.
- 💾 Data is stored in a JSON file (`journal.json`) with human-readable formatting.
- 🕒 Timestamps are automatically added and updated.
- No external dependencies – uses only Python standard library.

---

## Project Structure

```
journal_app/
├── models/
│   ├── __init__.py
│   └── entry.py
├── services/
│   ├── __init__.py
│   └── journal_service.py
├── storage/
│   ├── __init__.py
│   └── file_storage.py
└── main.py
```

- **`models/`** – Data classes (`Entry`).
- **`services/`** – Business logic (`JournalService` manages entries and validation).
- **`storage/`** – File read/write operations (`FileStorage`).
- **`main.py`** – Command-line interface and menu loop.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses only the standard library)

### Running the Application

1. Clone or download this repository.
2. Open a terminal in the `journal_app` folder.
3. Run:

```bash
python main.py
```

The first run will create a `journal.json` file.

---

## Usage

When you run the program, you'll see a menu:

```
--- Journal App ---
1. New Entry
2. View All Entries
3. View Single Entry
4. Search Entries
5. Edit Entry
6. Delete Entry
7. Exit
Choose:
```

### New Entry

Enter a title, content, and optional tags (comma-separated). The entry is saved with a timestamp.

### View All Entries

Shows a list of all entries with ID, title, and timestamp.

### View Single Entry

Enter an ID to see full details (title, content, tags, timestamp).

### Search Entries

Enter a search term; it matches against title, content, or tags.

### Edit Entry

Provide the ID and new values. Leave blank to keep current value. The timestamp is updated on edit.

### Delete Entry

Enter the ID to remove an entry.

---

## How It Works

### File Storage

`FileStorage` handles all JSON file operations using the `pathlib` module. It loads the file into a list of dictionaries and converts them to `Entry` objects. When saving, it converts back to dictionaries and writes with indentation.

### Service Layer

`JournalService` keeps an in-memory list of entries for fast access. It synchronizes with the file after every create, update, or delete. Business rules (like non-empty title) are enforced here.

### Data Persistence

The JSON file contains an array of entry objects. Each object includes `id`, `title`, `content`, `timestamp`, and `tags`. The file is created automatically if missing.

---

## Extending the Project

Here are some ideas to enhance the application:

- Export all entries to a plain text file.
- Filter entries by date range or tag.
- Add entry categories or moods.
- Implement encryption for privacy.
- Add a simple GUI using Tkinter.
- Write unit tests for the service layer.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy journaling! 📔🐍