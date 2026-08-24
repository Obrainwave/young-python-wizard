# Contact Book

A command-line application for managing personal contacts. You can add, view, search, update, and delete contacts. Built with Python and SQLite, this project demonstrates a clean object-oriented architecture with separated models, services, and storage layers.

This project is part of the **Young Python Wizard** series and is designed to teach how to build maintainable, production-ready applications.

---

## Features

- 👤 Add contacts with name, phone, email, and address.
- 📋 View all contacts in a formatted list.
- 🔍 Search contacts by name, phone, or email.
- ✏️ Update existing contact information.
- 🗑️ Delete contacts.
- 💾 Persistent storage using SQLite (no external dependencies).

---

## Project Structure

```
contact_book/
├── models/
│   ├── __init__.py
│   └── contact.py
├── services/
│   ├── __init__.py
│   └── contact_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   └── contact_repository.py
└── main.py
```

- **`models/`** – Data classes (e.g., `Contact`).
- **`services/`** – Business logic (validation, search, update operations).
- **`storage/`** – Database connection, initialization, and repository.
- **`main.py`** – Command-line interface and menu loop.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses only the standard library)

### Running the Application

1. Clone or download this repository.
2. Open a terminal in the `contact_book` folder.
3. Run:

```bash
python main.py
```

The first run will create a database file named `contacts.db`.

---

## Usage

When you run the program, you'll see a menu:

```
--- Contact Book ---
1. Add Contact
2. View All Contacts
3. Search Contacts
4. Update Contact
5. Delete Contact
6. Exit
Choose:
```

### Add a Contact

Enter the name (required) and optionally phone, email, and address. The system assigns a unique ID.

### View All Contacts

Displays all contacts sorted by name, showing all details.

### Search Contacts

Enter a search term. The app searches by name, phone, or email (case-insensitive) and shows matching contacts.

### Update Contact

Provide the contact ID. You can enter new values or leave blank to keep current values. The app updates the record.

### Delete Contact

Enter the contact ID to delete it.

---

## How It Works

### Database Initialization

`DatabaseInitializer` checks whether the `contacts` table exists. If not, it creates it. This avoids redundant `CREATE TABLE` operations on every startup.

### Layered Architecture

- **Repositories** (in `storage/`) handle all SQL queries. They insert, update, delete, and fetch data, converting rows to `Contact` objects.
- **Services** (in `services/`) contain business logic and validation. For example, `ContactService.add_contact()` ensures the name is non-empty and strips whitespace.
- **Models** are simple data containers with no database knowledge.

### Search Implementation

The search uses SQL `LIKE` with wildcard `%term%` to match partial strings in name, phone, or email.

---

## Extending the Project

Here are some ideas to enhance the application and practise your skills:

- Add input validation (phone format, email format).
- Allow sorting contacts by different fields.
- Add tags or categories for contacts.
- Export contacts to CSV or JSON.
- Detect duplicate contacts when adding.
- Build a graphical interface using Tkinter.
- Write unit tests using `pytest` with an in-memory SQLite database.

---

## Full Source Code

The complete code is available on GitHub:  
[https://github.com/Obrainwave/young-python-wizard/projects/contact_book](https://github.com/Obrainwave/young-python-wizard/projects/contact_book)

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy coding! 📇🐍