class Enrollment:
    def __init__(self, enrollment_id=None, student_id=None, course_id=None, grade="", enrolled_on=""):
        self.id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade
        self.enrolled_on = enrolled_on

    def __repr__(self):
        return f"Enrollment(id={self.id}, student_id={self.student_id}, course_id={self.course_id}, grade='{self.grade}')"