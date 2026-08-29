from models.project import Project
from models.technology import Technology
from storage.project_repository import ProjectRepository
from storage.technology_repository import TechnologyRepository

class PortfolioService:
    def __init__(self, db):
        self.project_repo = ProjectRepository(db)
        self.tech_repo = TechnologyRepository(db)

    def add_project(self, title, description, github_url, demo_url, date_created, featured, tech_names):
        # Validate title
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        # Create Technology objects from names
        tech_objects = [Technology(name=name.strip()) for name in tech_names if name.strip()]
        project = Project(
            title=title.strip(),
            description=description.strip(),
            github_url=github_url.strip(),
            demo_url=demo_url.strip(),
            date_created=date_created.strip(),
            featured=featured,
            technologies=tech_objects
        )
        return self.project_repo.insert(project)

    def get_all_projects(self):
        return self.project_repo.get_all()

    def get_project(self, project_id):
        return self.project_repo.get_by_id(project_id)

    def search_projects(self, term):
        return self.project_repo.search(term)

    def filter_by_technology(self, tech_name):
        return self.project_repo.get_by_technology(tech_name)

    def update_project(self, project_id, title, description, github_url, demo_url, date_created, featured, tech_names):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        project.title = title.strip()
        project.description = description.strip()
        project.github_url = github_url.strip()
        project.demo_url = demo_url.strip()
        project.date_created = date_created.strip()
        project.featured = featured
        project.technologies = [Technology(name=name.strip()) for name in tech_names if name.strip()]
        self.project_repo.update(project)
        return project

    def delete_project(self, project_id):
        if not self.project_repo.get_by_id(project_id):
            return False
        self.project_repo.delete(project_id)
        return True

    def get_all_technologies(self):
        return self.tech_repo.get_all()

    def export_to_html(self, filename="portfolio.html"):
        """Export all projects to an HTML file."""
        projects = self.project_repo.get_all()
        with open(filename, "w") as f:
            f.write("<html><head><title>My Portfolio</title>")
            f.write("<style>body{font-family:sans-serif;} .project{border:1px solid #ccc; margin:10px; padding:10px;}</style>")
            f.write("</head><body><h1>My Projects</h1>")
            for p in projects:
                f.write(f"<div class='project'><h2>{p.title}</h2>")
                if p.featured:
                    f.write("<strong>Featured</strong>")
                f.write(f"<p>{p.description}</p>")
                if p.github_url:
                    f.write(f"<p><a href='{p.github_url}'>GitHub</a></p>")
                if p.demo_url:
                    f.write(f"<p><a href='{p.demo_url}'>Live Demo</a></p>")
                f.write(f"<p><small>Date: {p.date_created}</small></p>")
                if p.technologies:
                    f.write("<p>Technologies: " + ", ".join(t.name for t in p.technologies) + "</p>")
                f.write("</div>")
            f.write("</body></html>")
        return filename