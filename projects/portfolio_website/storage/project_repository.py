from models.project import Project

class ProjectRepository:
    def __init__(self, db):
        self._db_getter = db

    @property
    def db(self):
        return self._db_getter() if callable(self._db_getter) else self._db_getter

    def insert(self, project):
        self.db.execute(
            "INSERT INTO projects (title, description, image_url, github_url, live_url, date_created, featured) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (project.title, project.description, project.image_url, project.github_url,
             project.live_url, project.date_created, 1 if project.featured else 0)
        )
        self.db.commit()
        project.id = self.db.last_row_id()
        return project

    def get_by_id(self, project_id):
        self.db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = self.db.fetchone()
        if row:
            return self._row_to_project(row)
        return None

    def get_all(self):
        self.db.execute("SELECT * FROM projects ORDER BY date_created DESC")
        rows = self.db.fetchall()
        return [self._row_to_project(row) for row in rows]

    def get_featured(self):
        self.db.execute("SELECT * FROM projects WHERE featured = 1 ORDER BY date_created DESC")
        rows = self.db.fetchall()
        return [self._row_to_project(row) for row in rows]

    def update(self, project):
        self.db.execute(
            "UPDATE projects SET title = ?, description = ?, image_url = ?, github_url = ?, "
            "live_url = ?, date_created = ?, featured = ? WHERE id = ?",
            (project.title, project.description, project.image_url, project.github_url,
             project.live_url, project.date_created, 1 if project.featured else 0, project.id)
        )
        self.db.commit()

    def delete(self, project_id):
        self.db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.db.commit()

    def _row_to_project(self, row):
        return Project(
            project_id=row["id"],
            title=row["title"],
            description=row["description"],
            image_url=row["image_url"],
            github_url=row["github_url"],
            live_url=row["live_url"],
            date_created=row["date_created"],
            featured=bool(row["featured"])
        )