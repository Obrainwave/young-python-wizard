from models.enrollment import Enrollment
from storage.enrollment_repository import EnrollmentRepository
from storage.student_repository import StudentRepository
from storage.course_repository import CourseRepository

class EnrollmentService:
    def __init__(self, db_path):
        self.repo = EnrollmentRepository(db_path)
        self.student_repo = StudentRepository(db_path)
        self.course_repo = CourseRepository(db_path)

    def enroll_student(self, student_id, course_id, grade="", enrolled_on=""):
        if not self.student_repo.get_by_id(student_id):
            raise ValueError("Student not found.")
        if not self.course_repo.get_by_id(course_id):
            raise ValueError("Course not found.")
        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
            grade=grade.strip(),
            enrolled_on=enrolled_on.strip()
        )
        return self.repo.insert(enrollment)

    def get_all_enrollments(self):
        return self.repo.get_all()

    def get_enrollment(self, enrollment_id):
        return self.repo.get_by_id(enrollment_id)

    def get_enrollments_by_student(self, student_id):
        return self.repo.get_by_student(student_id)

    def get_enrollments_by_course(self, course_id):
        return self.repo.get_by_course(course_id)

    def update_enrollment(self, enrollment_id, student_id, course_id, grade, enrolled_on):
        enrollment = self.repo.get_raw_by_id(enrollment_id)
        if not enrollment:
            raise ValueError("Enrollment not found.")
        if not self.student_repo.get_by_id(student_id):
            raise ValueError("Student not found.")
        if not self.course_repo.get_by_id(course_id):
            raise ValueError("Course not found.")
        enrollment.student_id = student_id
        enrollment.course_id = course_id
        enrollment.grade = grade.strip()
        enrollment.enrolled_on = enrolled_on.strip()
        self.repo.update(enrollment)
        return enrollment

    def delete_enrollment(self, enrollment_id):
        if not self.repo.get_raw_by_id(enrollment_id):
            return False
        self.repo.delete(enrollment_id)
        return True