# Quiz Application

A command-line application for creating quizzes, adding multiple-choice questions, taking quizzes interactively, and viewing results. Built with Python and SQLite, this project demonstrates clean object-oriented architecture with separated models, services, and storage layers.

This project is part of the **Young Python Wizard** series and is designed to teach how to build maintainable, production-ready applications.

---

## Features

- 📝 Create and manage quizzes with title and description.
- ❓ Add multiple-choice questions (4 options, one correct answer).
- 🎯 Take quizzes interactively with immediate feedback.
- 🧮 Automatically calculate and store quiz scores.
- 📊 View past results for any quiz.
- 💾 Persistent storage using SQLite (no external dependencies).

---

## Project Structure

```
quiz_application/
├── models/
│   ├── __init__.py
│   ├── quiz.py
│   ├── question.py
│   └── quiz_result.py
├── services/
│   ├── __init__.py
│   └── quiz_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── quiz_repository.py
│   ├── question_repository.py
│   └── result_repository.py
└── main.py
```

- **`models/`** – Data classes (`Quiz`, `Question`, `QuizResult`).
- **`services/`** – Business logic (quiz creation, question management, quiz taking, scoring).
- **`storage/`** – Database connection, initialization, and repositories.
- **`main.py`** – Command-line interface and menu loop.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses only the standard library)

### Running the Application

1. Clone or download this repository.
2. Open a terminal in the `quiz_application` folder.
3. Run:

```bash
python main.py
```

The first run will create a database file named `quiz.db`.

---

## Usage

When you run the program, you'll see a menu:

```
--- Quiz Application ---
1. Create Quiz
2. View All Quizzes
3. Add Question to Quiz
4. Take Quiz
5. View Results for Quiz
6. Delete Quiz
7. Exit
Choose:
```

### Create a Quiz

Provide a title and optional description. The system assigns a unique ID.

### Add Question to a Quiz

Select a quiz by ID, then enter:
- Question text
- Four options (you will be prompted for each)
- Correct option number (1–4)

The options are stored as JSON in the database.

### Take a Quiz

Enter the quiz ID. The app displays each question and options. Answer by entering the option number. You receive immediate feedback ("Correct!" or "Wrong."). At the end, your score is displayed and saved.

### View Results

Enter a quiz ID to see past attempts with timestamps and scores.

---

## How It Works

### Database Initialization

`DatabaseInitializer` checks whether the required tables (`quizzes`, `questions`, `results`) exist. If any are missing, it creates all tables. This prevents redundant `CREATE TABLE` statements on every run.

### Layered Architecture

- **Repositories** (in `storage/`) handle all SQL queries. They insert, update, delete, and fetch records, converting rows to model objects.
- **Services** (in `services/`) contain the business logic. For example, `QuizService.take_quiz()` handles the quiz loop, calculates the score, and saves the result.
- **Models** are simple data containers with no database knowledge.

### Question Options Storage

The `options` list for each question is serialized to a JSON string using `json.dumps` before saving. When reading, `json.loads` converts it back to a list.

---

## Extending the Project

Here are some ideas to enhance the application and practise your skills:

- Add edit functionality for quizzes and questions.
- Support deleting individual questions.
- Shuffle question order when taking a quiz.
- Store which questions were answered incorrectly in results.
- Show best score or average score per quiz.
- Export results to CSV.
- Write unit tests using `pytest` with an in-memory SQLite database.

---

## Full Source Code

The complete code is available on GitHub:  
[https://github.com/Obrainwave/young-python-wizard/projects/quiz_application](https://github.com/Obrainwave/young-python-wizard/projects/quiz_application)

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy coding! 📚🐍