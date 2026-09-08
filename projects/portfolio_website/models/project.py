class Project:
    def __init__(self, project_id=None, title="", description="", image_url="", 
                 github_url="", live_url="", date_created="", featured=False):
        self.id = project_id
        self.title = title
        self.description = description
        self.image_url = image_url
        self.github_url = github_url
        self.live_url = live_url
        self.date_created = date_created
        self.featured = featured

    def __repr__(self):
        return f"Project(id={self.id}, title='{self.title}', featured={self.featured})"