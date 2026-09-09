class Student:
    def __init__(self, student_id=None, name="", email="", phone=""):
        self.id = student_id
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}')"