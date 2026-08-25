# Library Management System

A command-line application for managing a library's books, members, and borrowing records. It supports adding book cover images, searching, borrowing/returning books, and tracking overdue loans. Built with Python and SQLite, this project demonstrates clean object-oriented architecture with separated models, services, and storage layers.

This project is part of the **Young Python Wizard** series and is designed to teach how to build maintainable, production-ready applications.

---

## Features

- 📚 Manage books: add, search, list, update, delete.
- 🖼️ Store and manage book cover images (file-based storage).
- 👥 Manage members: add, list, search.
- 🔄 Borrow and return books with automatic due dates (14 days).
- ⏰ View overdue loans.
- 💾 Persistent storage using SQLite (no external dependencies beyond standard library).

---

## Project Structure

```
library_management/
├── models/
│   ├── __init__.py
│   ├── book.py
│   ├── member.py
│   └── loan.py
├── services/
│   ├── __init__.py
│   └── library_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── book_repository.py
│   ├── member_repository.py
│   └── loan_repository.py
├── book_covers/           # created automatically; stores cover images
└── main.py
```

- **`models/`** – Data classes (`Book`, `Member`, `Loan`).
- **`services/`** – Business logic (validation, borrowing/returning rules, cover handling).
- **`storage/`** – Database connection, initialization, and repositories.
- **`book_covers/`** – Directory where cover images are stored.
- **`main.py`** – Command-line interface and menu loop.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses only the standard library)

### Running the Application

1. Clone or download this repository.
2. Open a terminal in the `library_management` folder.
3. Run:

```bash
python main.py
```

The first run will create a database file named `library.db` and a `book_covers` folder.

---

## Usage

When you run the program, you'll see a menu:

```
--- Library Management System ---
1. Manage Books
2. Manage Members
3. Borrow Book
4. Return Book
5. View Overdue Loans
6. Exit
Choose:
```

### Manage Books

From this submenu you can:
- **Add Book**: enter title, author, ISBN (optional), and optionally a path to a cover image file.
- **Search Books**: search by title, author, or ISBN.
- **List All Books**: display all books with availability and cover status.
- **Update Book Info**: modify title, author, ISBN.
- **Add/Update Cover**: assign or change the cover image for a book.
- **Delete Book**: remove a book (only if not currently borrowed).

### Manage Members

Add, list, or search members by name or email.

### Borrow Book

Choose an available book and enter member ID. The system sets a due date 14 days from today.

### Return Book

Enter the book ID to mark it as returned and make it available again.

### View Overdue Loans

Shows active loans whose due date has passed.

---

## How It Works

### Database Initialization

`DatabaseInitializer` checks whether the required tables (`books`, `members`, `loans`) exist. If any are missing, it creates all tables and also creates the `book_covers` directory if needed.

### Book Cover Handling

- Cover images are stored as files in the `book_covers` folder.
- The database stores the file path (not the binary data).
- When adding or updating a cover, the service copies the provided image file to the `book_covers` directory using a sanitized filename based on the book title.
- When deleting a book, the associated cover file is also removed from disk.

### Layered Architecture

- **Repositories** handle SQL operations and convert rows to model objects.
- **Services** contain business logic: validation, borrowing rules, due dates, and cover management.
- **Models** are simple data containers.

### Borrowing Logic

- A book can only be borrowed if `available` is `True`.
- Borrowing creates a loan record with `returned = 0` and sets the book's `available` to `False`.
- Returning finds the active loan, marks it returned, and sets the book back to available.
- Overdue loans are those with `returned = 0` and `due_date < today`.

---

## Extending the Project

Here are some ideas to enhance the application and practise your skills:

- Add fine calculation for overdue books.
- Validate cover images (check file extension or use PIL).
- Implement reservations for borrowed books.
- Export book or loan data to CSV.
- Write unit tests using `pytest` with an in-memory SQLite database.
- Build a graphical interface using Tkinter that displays book covers.
- Add barcode scanning for ISBN entry.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy coding! 📖🐍