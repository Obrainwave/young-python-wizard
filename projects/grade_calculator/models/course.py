class Course:
    def __init__(self, course_id=None, name=""):
        self.id = course_id
        self.name = name

    def __repr__(self):
        return f"Course(id={self.id}, name='{self.name}')"