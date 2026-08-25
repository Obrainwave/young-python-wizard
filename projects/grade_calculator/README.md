# Grade Calculator

A command-line application for managing students, courses, assignments, and calculating weighted grades. Built with Python and SQLite, this project demonstrates a professional, object-oriented architecture with separated models, services, and storage layers.

This project is part of the **Young Python Wizard** series and is designed to teach how to build maintainable, production-ready applications.

---

## Features

- 👩‍🎓 Manage students (add, view, update, delete).
- 📚 Manage courses.
- 📝 Create assignments linked to courses with max score and weight.
- 🎯 Record scores for students on assignments (supports upsert).
- 🧮 Calculate weighted averages and letter grades.
- 📊 View student reports with per-course performance.
- 💾 Persist all data in a local SQLite database.

---

## Project Structure

```
grade_calculator/
├── models/
│   ├── __init__.py
│   ├── student.py
│   ├── course.py
│   └── assignment.py
├── services/
│   ├── __init__.py
│   └── grade_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── student_repository.py
│   ├── course_repository.py
│   ├── assignment_repository.py
│   └── score_repository.py
└── main.py
```

- **`models/`** – Plain Python classes that represent real-world entities (`Student`, `Course`, `Assignment`).
- **`services/`** – Business logic (grade calculations, validation, orchestration).
- **`storage/`** – Database connection, schema initialization, and repositories for each entity.
- **`main.py`** – Command-line interface and menu loop.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses only the standard library)

### Running the Application

1. Clone or download this repository.
2. Open a terminal in the `grade_calculator` folder.
3. Run:

```bash
python main.py
```

The first run will create a database file named `gradebook.db`.

---

## Usage

When you run the program, you'll see a menu:

```
--- Grade Calculator ---
1. Add Student
2. View Students
3. Add Course
4. View Courses
5. Add Assignment to Course
6. Record Score
7. Student Report
8. Exit
Choose:
```

### Add a Student

Enter the student's name. The system assigns a unique ID automatically.

### Add a Course

Enter the course name. The system assigns a unique ID.

### Add an Assignment to a Course

Provide:

- Course ID (must exist)
- Assignment name
- Maximum score
- Weight as a decimal (e.g., 0.2 for 20% of the total grade)

### Record a Score

Provide:

- Student ID
- Assignment ID
- Score (must be between 0 and the assignment's max score)

If a score already exists for that student and assignment, it will be updated.

### View Student Report

Enter a student ID. The system calculates the weighted average for each course and displays the letter grade (A–F).

---

## How It Works

### Database Initialization

The `DatabaseInitializer` class checks whether the required tables already exist using SQLite's `sqlite_master` table. If they do, no action is taken. If any table is missing, all tables are created. This avoids redundant `CREATE TABLE` statements on every startup.

### Layered Architecture

- **Repositories** (in `storage/`) handle all SQL queries. They insert, update, delete, and fetch data, converting rows to model objects.
- **Services** (in `services/`) contain the business logic. For example, `GradeService.calculate_weighted_average()` retrieves assignments and scores, then computes the weighted grade.
- **Models** are simple data containers with no database knowledge.

### Grade Calculation

The weighted average for a student in a course is calculated as:

```
weighted_average = (Σ (score / max_score) * weight) / Σ weight) * 100
```

Only assignments with recorded scores are included. Letter grades are assigned based on standard thresholds (A: ≥90, B: ≥80, C: ≥70, D: ≥60, F: <60).

---

## Extending the Project

Here are some ideas to enhance the application and practise your skills:

- Add input validation (e.g., weight between 0 and 1, positive max score).
- Generate course reports showing all students and their grades.
- Implement edit/delete operations for all entities.
- Support grading categories (e.g., Homework, Exams) with separate weights.
- Export reports to CSV or PDF.
- Write unit tests using `pytest` with an in-memory SQLite database.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy coding! 🎓🐍