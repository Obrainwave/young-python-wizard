class Student:
    def __init__(self, student_id=None, name=""):
        self.id = student_id
        self.name = name

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}')"

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)