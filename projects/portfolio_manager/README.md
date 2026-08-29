# Developer Portfolio Manager

A command-line application to manage and showcase your coding projects. Store project details, tag technologies, mark featured projects, search and filter, and export to a static HTML portfolio page. Built with Python and SQLite, this project demonstrates advanced object-oriented design with a many-to-many relationship and layered architecture.

This is the capstone project of the **Young Python Wizard** Module 7 series.

---

## Features

- 🚀 Add, view, edit, and delete projects.
- 🏷️ Tag projects with multiple technologies.
- 🔍 Search by title, description, or technology.
- ⭐ Mark projects as featured.
- 📤 Export your entire portfolio to a styled HTML file.
- 💾 Persistent storage using SQLite.

---

## Project Structure

```
portfolio_manager/
├── models/
│   ├── __init__.py
│   ├── project.py
│   └── technology.py
├── services/
│   ├── __init__.py
│   └── portfolio_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── project_repository.py
│   └── technology_repository.py
├── export_template.html
└── main.py
```

- **`models/`** – Data classes (`Project`, `Technology`).
- **`services/`** – Business logic (`PortfolioService`).
- **`storage/`** – Database connection, initialization, and repositories.
- **`export_template.html`** – Optional HTML template for export.
- **`main.py`** – Command-line interface.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies

---

### Running

```bash
python main.py
```

The first run creates `portfolio.db`.

---

## Usage

Menu options:

1. **Add Project** – enter title, description, URLs, date, featured status, and comma-separated technologies.
2. **View All Projects** – list all projects with ID, title, and featured flag.
3. **View Single Project** – display full details by ID.
4. **Search Projects** – search across title, description, and technologies.
5. **Filter by Technology** – list projects that use a specific technology.
6. **Edit Project** – update any field (blank keeps current value).
7. **Delete Project** – remove a project.
8. **Export to HTML** – generate `portfolio.html` with all projects.
9. **Exit**

---

## Database Schema

Three tables:
- `projects` – id, title, description, github_url, demo_url, date_created, featured.
- `technologies` – id, name (unique).
- `project_technologies` – composite primary key linking projects and technologies.

---

## Export Feature

The export feature creates a styled `portfolio.html` file. You can replace the direct string building in `portfolio_service.py` with the provided `export_template.html` for a more flexible template-based approach.

---

## Extending

Ideas to enhance:
- Add categories.
- Sorting options.
- Export to JSON.
- GUI with Tkinter or Flask.
- Screenshot support.

---

## License

Part of the **Young Python Wizard** learning repository. Free for personal and educational use.
