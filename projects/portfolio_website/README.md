# Professional Portfolio Website

A full-featured portfolio website built with Flask and SQLite. It includes a public-facing project showcase and an admin panel for managing content. The project follows a clean layered architecture with separate models, services, storage, and web application layers.

This project is part of the **Young Python Wizard** Module 9 series.

---

## Features

- 🏠 Public home page displaying all projects in a responsive grid.
- 📄 Project detail pages with full information and external links.
- ⭐ Featured project highlighting.
- 🔐 Admin panel (no authentication yet—see extensions) for CRUD operations.
- 🗄️ SQLite database for persistent storage.
- 🎨 Modern Bootstrap 5 UI with custom CSS.
- 📁 Clean separation of concerns (models, services, storage, webapp).

---

## Project Structure

```
portfolio_website/
├── models/
│   ├── __init__.py
│   └── project.py
├── services/
│   ├── __init__.py
│   └── project_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   └── project_repository.py
├── webapp/
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── project_detail.html
│   │   ├── admin.html
│   │   └── edit_project.html
│   └── static/
│       ├── style.css
│       └── images/
├── main.py
└── requirements.txt
```

- **`models/`** – Data classes (`Project`).
- **`services/`** – Business logic (`ProjectService`).
- **`storage/`** – Database connection, initialization, and repository.
- **`webapp/`** – Flask application factory, routes, templates, and static assets.
- **`main.py`** – Entry point that runs the Flask app.

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

On first run, the database (`portfolio.db`) and tables are created automatically.

---

## Usage

### Public Pages

- **Home** (`/`): Displays all projects in a card grid. Featured projects show a badge.
- **Project Detail** (`/project/<id>`): Shows full project description, image, and links.

### Admin Panel

- **Admin** (`/admin`): Lists all projects with edit/delete actions.
- **Add Project** (`/admin/add`): Form to create a new project.
- **Edit Project** (`/admin/edit/<id>`): Form to update an existing project.
- **Delete Project**: Via POST button in admin list.

### Adding Images

Place image files in `webapp/static/images/`. In the admin form, enter just the filename (e.g., `myproject.jpg`) in the "Image Filename" field.

---

## How It Works

### Application Factory

`webapp/__init__.py` defines a `create_app()` factory that:
- Creates the Flask app.
- Connects to the database.
- Initializes tables if needed.
- Instantiates the `ProjectService`.
- Registers blueprint routes.

### Layered Architecture

- **Repository** (`storage/project_repository.py`) handles all SQL queries.
- **Service** (`services/project_service.py`) contains business logic and validation.
- **Models** (`models/project.py`) are simple data containers.
- **Routes** (`webapp/routes.py`) handle HTTP requests and render templates.

### Database

Uses SQLite with a single `projects` table. The schema is created automatically by `DatabaseInitializer` if it doesn't exist.

---

## Extending the Project

Here are ideas to enhance the site:

- Add authentication to the admin panel (Flask-Login).
- Support image uploads directly in the form.
- Add categories or tags for projects.
- Implement pagination for many projects.
- Create JSON API endpoints (`/api/projects`).
- Add a search bar.
- Deploy to PythonAnywhere or Heroku.
- Write unit tests using `pytest`.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy building! 🌐🐍
