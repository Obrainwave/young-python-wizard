class Assignment:
    def __init__(self, assignment_id=None, course_id=None, name="", max_score=100.0, weight=1.0):
        self.id = assignment_id
        self.course_id = course_id
        self.name = name
        self.max_score = max_score
        self.weight = weight

    def __repr__(self):
        return f"Assignment(id={self.id}, course_id={self.course_id}, name='{self.name}', max_score={self.max_score}, weight={self.weight})"