# Student Management System

A web application for managing students, courses, and enrollments. Built with Flask and SQLite, this project follows a clean layered architecture with separate models, services, storage, and web layers.

This project is part of the **Young Python Wizard** Module 9 series.

---

## Features

- 🧑‍🎓 Student management: add, view, edit, delete, search students.
- 📚 Course management: add, view, edit, delete, search courses.
- 📝 Enrollment management: enroll students in courses, record grades, edit, delete.
- 🔍 Search and filter students and courses.
- 📊 View student details with their enrollments.
- 📈 View course details with enrolled students.
- 💾 SQLite database for persistent storage.
- 🎨 Modern Bootstrap 5 UI.

---

## Project Structure

```
student_management/
├── models/
│   ├── __init__.py
│   ├── student.py
│   ├── course.py
│   └── enrollment.py
├── services/
│   ├── __init__.py
│   ├── student_service.py
│   ├── course_service.py
│   └── enrollment_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── student_repository.py
│   ├── course_repository.py
│   └── enrollment_repository.py
├── webapp/
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── students.html
│   │   ├── student_form.html
│   │   ├── student_detail.html
│   │   ├── courses.html
│   │   ├── course_form.html
│   │   ├── course_detail.html
│   │   ├── enrollments.html
│   │   └── enrollment_form.html
│   └── static/
│       └── style.css
├── main.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

Open `http://127.0.0.1:5000` in your browser.

The database (`student_management.db`) and tables are created automatically on first run.

---

## Usage

### Students

- Navigate to `/students` to view all students.
- Use the search bar to find by name or email.
- Click "Add Student" to create a new student.
- Click a student's name to view details and enrollments.
- Use Edit/Delete buttons for modifications.

### Courses

- Navigate to `/courses` to view all courses.
- Search by title or description.
- Add, edit, or delete courses.

### Enrollments

- Navigate to `/enrollments` to view all enrollments with student and course names.
- Add new enrollments by selecting student and course, entering grade and date.
- Edit or delete existing enrollments.

---

## How It Works

### Layered Architecture

- **Repository** (in `storage/`) handles all SQL queries. Each method opens a new connection for thread safety.
- **Service** (in `services/`) contains business logic and validation.
- **Models** are simple data containers.
- **Routes** (in `webapp/routes.py`) handle HTTP requests and render templates.

### Database

SQLite database with three tables: `students`, `courses`, `enrollments`. The schema is created automatically by `DatabaseInitializer` if it doesn't exist.

---

## Extending the Project

- Add user authentication.
- Implement GPA calculation from grades.
- Generate PDF reports.
- Add pagination for large datasets.
- Add attendance tracking.
- Deploy to PythonAnywhere or Heroku.
- Write unit tests using `pytest`.

---

## Full Source Code

The complete code is available on GitHub:  
[https://github.com/Obrainwave/young-python-wizard/projects/student_management](https://github.com/Obrainwave/young-python-wizard/projects/student_management)

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy coding! 🎓🐍
```