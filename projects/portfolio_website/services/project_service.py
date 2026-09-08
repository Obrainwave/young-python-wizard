from models.project import Project
from storage.project_repository import ProjectRepository

class ProjectService:
    def __init__(self, db):
        self.repo = ProjectRepository(db)

    def create_project(self, title, description, image_url="", github_url="", live_url="", date_created="", featured=False):
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        project = Project(
            title=title.strip(),
            description=description.strip(),
            image_url=image_url.strip(),
            github_url=github_url.strip(),
            live_url=live_url.strip(),
            date_created=date_created.strip(),
            featured=featured
        )
        return self.repo.insert(project)

    def get_project(self, project_id):
        return self.repo.get_by_id(project_id)

    def get_all_projects(self):
        return self.repo.get_all()

    def get_featured_projects(self):
        return self.repo.get_featured()

    def update_project(self, project_id, title, description, image_url="", github_url="", live_url="", date_created="", featured=False):
        project = self.repo.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        project.title = title.strip()
        project.description = description.strip()
        project.image_url = image_url.strip()
        project.github_url = github_url.strip()
        project.live_url = live_url.strip()
        project.date_created = date_created.strip()
        project.featured = featured
        self.repo.update(project)
        return project

    def delete_project(self, project_id):
        project = self.repo.get_by_id(project_id)
        if not project:
            return False
        self.repo.delete(project_id)
        return True