from models.student import Student
from storage.student_repository import StudentRepository

class StudentService:
    def __init__(self, db_path):
        self.repo = StudentRepository(db_path)

    def create_student(self, name, email="", phone=""):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        student = Student(name=name.strip(), email=email.strip(), phone=phone.strip())
        return self.repo.insert(student)

    def get_student(self, student_id):
        return self.repo.get_by_id(student_id)

    def get_all_students(self):
        return self.repo.get_all()

    def search_students(self, term):
        return self.repo.search(term)

    def update_student(self, student_id, name, email="", phone=""):
        student = self.repo.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found.")
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        student.name = name.strip()
        student.email = email.strip()
        student.phone = phone.strip()
        self.repo.update(student)
        return student

    def delete_student(self, student_id):
        if not self.repo.get_by_id(student_id):
            return False
        self.repo.delete(student_id)
        return True