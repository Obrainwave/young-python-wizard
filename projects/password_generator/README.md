# Password Generator

A command-line application that generates strong, random passwords based on your preferences. You can choose the length and which character types to include (uppercase, lowercase, digits, special characters). The app also keeps a history of generated passwords using SQLite.

This project is part of the **Young Python Wizard** series and follows professional software architecture: separated models, services, and storage layers.

---

## Features

- 🔐 Generate cryptographically secure passwords using Python's `secrets` module.
- ⚙️ Choose password length and character types:
  - Uppercase letters (A–Z)
  - Lowercase letters (a–z) — always included
  - Digits (0–9)
  - Special characters (!, @, #, etc.)
- 📜 Save generated passwords to a local SQLite database.
- 👀 View password history (newest first).
- 🧹 Clear the history.

---

## Project Structure

```
password_generator/
├── models/
│   ├── __init__.py
│   └── password_history.py
├── services/
│   ├── __init__.py
│   └── password_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   └── password_history_repository.py
└── main.py
```

- **`models/`** – Data classes (e.g., `PasswordHistory`).
- **`services/`** – Business logic (password generation, history management).
- **`storage/`** – Database connection and repository (SQLite).
- **`main.py`** – Command-line interface and menu.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses only the standard library)

### Running the Application

1. Clone or download this repository.
2. Open a terminal in the `password_generator` folder.
3. Run:

```bash
python main.py
```

The first run will create a database file named `password_history.db`.

---

## Usage

When you run the program, you'll see a menu:

```
--- Password Generator ---
1. Generate new password
2. View history
3. Clear history
4. Exit
Choose:
```

### Generate a New Password

1. Enter the desired password length (e.g., 12).
2. Answer `yes` or `no` to include:
   - Uppercase letters
   - Digits
   - Special characters
   - (Lowercase letters are always included)
3. The generated password will be displayed and automatically saved to history.

### View History

Shows a list of previously generated passwords with timestamp, length, and character types used.

### Clear History

Deletes all saved password records.

---

## How It Works

- **`PasswordService.generate_password()`** builds a pool of characters based on your choices and uses `secrets.choice()` to pick each character randomly. This method is suitable for security-sensitive applications.
- The generated password is stored in an SQLite database via `PasswordHistoryRepository`.
- `DatabaseInitializer` ensures the required table is created only if it doesn't already exist.

---

## Extending the Project

Here are some ideas to practise and improve the app:

- Add a password strength indicator.
- Copy the password to clipboard automatically (`pyperclip`).
- Allow custom character sets.
- Export history to CSV or text file.
- Write unit tests with `pytest`.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

---

Happy coding! 🐍🔒