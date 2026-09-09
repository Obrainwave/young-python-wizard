class Course:
    def __init__(self, course_id=None, title="", description="", credits=0):
        self.id = course_id
        self.title = title
        self.description = description
        self.credits = credits

    def __repr__(self):
        return f"Course(id={self.id}, title='{self.title}', credits={self.credits})"