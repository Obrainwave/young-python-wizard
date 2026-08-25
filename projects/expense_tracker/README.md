# Expense Tracker

A command-line application for tracking personal expenses by category. You can manage categories, record expenses with amounts and dates, filter expenses, and view summary reports. Built with Python and SQLite, this project demonstrates a clean object-oriented architecture with separated models, services, and storage layers.

This project is part of the **Young Python Wizard** series and is designed to teach how to build maintainable, production-ready applications.

---

## Features

- 🏷️ Manage expense categories (add, list, delete).
- 💸 Record expenses with amount, category, date, and optional description.
- 🔍 View all expenses or filter by category or date range.
- ✏️ Update or delete existing expenses.
- 📊 View total spending and spending by category.
- 💾 Persistent storage using SQLite (no external dependencies).

---

## Project Structure

```
expense_tracker/
├── models/
│   ├── __init__.py
│   ├── expense.py
│   └── category.py
├── services/
│   ├── __init__.py
│   └── expense_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── expense_repository.py
│   └── category_repository.py
└── main.py
```

- **`models/`** – Data classes (`Expense`, `Category`).
- **`services/`** – Business logic (validation, calculations, orchestration).
- **`storage/`** – Database connection, initialization, and repositories.
- **`main.py`** – Command-line interface and menu loop.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses only the standard library)

### Running the Application

1. Clone or download this repository.
2. Open a terminal in the `expense_tracker` folder.
3. Run:

```bash
python main.py
```

The first run will create a database file named `expenses.db`.

---

## Usage

When you run the program, you'll see a menu:

```
--- Expense Tracker ---
1. Manage Categories
2. Add Expense
3. View All Expenses
4. Filter Expenses
5. Update Expense
6. Delete Expense
7. View Summary
8. Exit
Choose:
```

### Manage Categories

Add, list, or delete categories. You cannot delete a category that has expenses associated with it.

### Add Expense

Select a category, enter amount, optional description, and date (leave blank for today). The system assigns a unique ID.

### View All Expenses

Displays all expenses sorted by date (newest first).

### Filter Expenses

Filter by category or by date range.

### Update Expense

Select an expense by ID, then modify its category, amount, description, or date.

### Delete Expense

Remove an expense by ID.

### View Summary

Shows total spent and a breakdown by category.

---

## How It Works

### Database Initialization

`DatabaseInitializer` checks whether the required tables (`categories`, `expenses`) exist. If not, it creates them. This avoids redundant `CREATE TABLE` operations on every run.

### Layered Architecture

- **Repositories** (in `storage/`) handle all SQL queries. They insert, update, delete, and fetch records, converting rows to model objects.
- **Services** (in `services/`) contain business logic and validation. For example, `ExpenseService.add_expense()` ensures the amount is positive, the category exists, and the date format is valid.
- **Models** are simple data containers with no database knowledge.

### Data Integrity

Expenses reference categories via foreign key. The service layer prevents deleting a category that still has expenses, maintaining referential integrity.

---

## Extending the Project

Here are some ideas to enhance the application and practise your skills:

- Add monthly or yearly summary reports.
- Implement budget alerts for categories or overall spending.
- Export expenses to CSV or JSON.
- Support recurring expenses.
- Add a graphical interface using Tkinter.
- Write unit tests using `pytest` with an in-memory SQLite database.
- Implement pagination for long expense lists.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy coding! 💰🐍