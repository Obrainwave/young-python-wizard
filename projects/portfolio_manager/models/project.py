class Project:
    def __init__(self, project_id=None, title="", description="", github_url="", demo_url="", date_created="", featured=False, technologies=None):
        self.id = project_id
        self.title = title
        self.description = description
        self.github_url = github_url
        self.demo_url = demo_url
        self.date_created = date_created
        self.featured = featured
        self.technologies = technologies if technologies is not None else []  # list of Technology objects

    def __repr__(self):
        return f"Project(id={self.id}, title='{self.title}', featured={self.featured})"