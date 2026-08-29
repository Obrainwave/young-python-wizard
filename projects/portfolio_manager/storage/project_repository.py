from models.project import Project
from models.technology import Technology

class ProjectRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, project):
        self.db.execute(
            "INSERT INTO projects (title, description, github_url, demo_url, date_created, featured) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (project.title, project.description, project.github_url, project.demo_url,
             project.date_created, 1 if project.featured else 0)
        )
        self.db.commit()
        project.id = self.db.last_row_id()
        # Insert technology associations
        self._insert_technologies(project)
        return project

    def _insert_technologies(self, project):
        for tech in project.technologies:
            tech_id = self._get_or_create_technology_id(tech.name)
            self.db.execute(
                "INSERT OR IGNORE INTO project_technologies (project_id, technology_id) VALUES (?, ?)",
                (project.id, tech_id)
            )
        self.db.commit()

    def _get_or_create_technology_id(self, tech_name):
        self.db.execute("SELECT id FROM technologies WHERE name = ?", (tech_name,))
        row = self.db.fetchone()
        if row:
            return row["id"]
        self.db.execute("INSERT INTO technologies (name) VALUES (?)", (tech_name,))
        self.db.commit()
        return self.db.last_row_id()

    def get_by_id(self, project_id):
        self.db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = self.db.fetchone()
        if not row:
            return None
        project = self._row_to_project(row)
        project.technologies = self._load_technologies(project.id)
        return project

    def get_all(self):
        self.db.execute("SELECT * FROM projects ORDER BY title")
        rows = self.db.fetchall()
        projects = []
        for row in rows:
            project = self._row_to_project(row)
            project.technologies = self._load_technologies(project.id)
            projects.append(project)
        return projects

    def search(self, term):
        # Search in title, description, or technology name
        self.db.execute("""
            SELECT DISTINCT p.* FROM projects p
            LEFT JOIN project_technologies pt ON p.id = pt.project_id
            LEFT JOIN technologies t ON pt.technology_id = t.id
            WHERE p.title LIKE ? OR p.description LIKE ? OR t.name LIKE ?
            ORDER BY p.title
        """, (f"%{term}%", f"%{term}%", f"%{term}%"))
        rows = self.db.fetchall()
        projects = []
        for row in rows:
            project = self._row_to_project(row)
            project.technologies = self._load_technologies(project.id)
            projects.append(project)
        return projects

    def get_by_technology(self, tech_name):
        self.db.execute("""
            SELECT DISTINCT p.* FROM projects p
            JOIN project_technologies pt ON p.id = pt.project_id
            JOIN technologies t ON pt.technology_id = t.id
            WHERE t.name = ?
            ORDER BY p.title
        """, (tech_name,))
        rows = self.db.fetchall()
        projects = []
        for row in rows:
            project = self._row_to_project(row)
            project.technologies = self._load_technologies(project.id)
            projects.append(project)
        return projects

    def update(self, project):
        self.db.execute(
            "UPDATE projects SET title = ?, description = ?, github_url = ?, demo_url = ?, date_created = ?, featured = ? WHERE id = ?",
            (project.title, project.description, project.github_url, project.demo_url,
             project.date_created, 1 if project.featured else 0, project.id)
        )
        self.db.commit()
        # Update technologies: clear existing then re-insert
        self.db.execute("DELETE FROM project_technologies WHERE project_id = ?", (project.id,))
        self._insert_technologies(project)

    def delete(self, project_id):
        self.db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.db.commit()

    def _row_to_project(self, row):
        return Project(
            project_id=row["id"],
            title=row["title"],
            description=row["description"],
            github_url=row["github_url"],
            demo_url=row["demo_url"],
            date_created=row["date_created"],
            featured=bool(row["featured"])
        )

    def _load_technologies(self, project_id):
        self.db.execute("""
            SELECT t.* FROM technologies t
            JOIN project_technologies pt ON t.id = pt.technology_id
            WHERE pt.project_id = ?
            ORDER BY t.name
        """, (project_id,))
        rows = self.db.fetchall()
        return [Technology(row["id"], row["name"]) for row in rows]