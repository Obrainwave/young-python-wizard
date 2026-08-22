from models.student import Student
from models.course import Course
from models.assignment import Assignment

from storage.student_repository import StudentRepository
from storage.course_repository import CourseRepository
from storage.assignment_repository import AssignmentRepository
from storage.score_repository import ScoreRepository

class GradeService:
    def __init__(self, db):
        self.student_repo = StudentRepository(db)
        self.course_repo = CourseRepository(db)
        self.assignment_repo = AssignmentRepository(db)
        self.score_repo = ScoreRepository(db)

    # Student operations
    def add_student(self, name):
        student = Student(name=name)
        return self.student_repo.insert(student)

    def get_all_students(self):
        return self.student_repo.get_all()

    def get_student(self, student_id):
        return self.student_repo.get_by_id(student_id)

    def update_student(self, student_id, name):
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found")
        student.name = name
        self.student_repo.update(student)

    def delete_student(self, student_id):
        # Also delete associated scores
        self.score_repo.delete_by_student(student_id)
        self.student_repo.delete(student_id)

    # Course operations
    def add_course(self, name):
        course = Course(name=name)
        return self.course_repo.insert(course)

    def get_all_courses(self):
        return self.course_repo.get_all()

    # Assignment operations
    def add_assignment(self, course_id, name, max_score, weight):
        try:
            # Validate course exists
            course = self.course_repo.get_by_id(course_id)
            if not course:
                raise ValueError("Course not found")
            assignment = Assignment(course_id=course_id, name=name, max_score=max_score, weight=weight)
            return self.assignment_repo.insert(assignment)
        except Exception as e:
            raise ValueError(f"Failed to add assignment: {e}")

    def get_assignments_for_course(self, course_id):
        return self.assignment_repo.get_by_course(course_id)

    # Score operations
    def record_score(self, student_id, assignment_id, score):
        # Validate assignment and student exist
        assignment = self.assignment_repo.get_by_id(assignment_id)
        if not assignment:
            raise ValueError("Assignment not found")
        if score < 0 or score > assignment.max_score:
            raise ValueError(f"Score must be between 0 and {assignment.max_score}")
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found")
        self.score_repo.upsert_score(student_id, assignment_id, score)

    def get_student_scores(self, student_id, course_id):
        assignments = self.assignment_repo.get_by_course(course_id)
        scores = {}
        for assignment in assignments:
            score = self.score_repo.get_score(student_id, assignment.id)
            if score is not None:
                scores[assignment.id] = score
        return scores

    # Grade calculation
    def calculate_weighted_average(self, student_id, course_id):
        assignments = self.assignment_repo.get_by_course(course_id)
        if not assignments:
            return None
        total_weight = 0.0
        weighted_sum = 0.0
        for assignment in assignments:
            score = self.score_repo.get_score(student_id, assignment.id)
            if score is not None:
                weighted_sum += (score / assignment.max_score) * assignment.weight
                total_weight += assignment.weight
        if total_weight == 0:
            return None
        return (weighted_sum / total_weight) * 100

    def letter_grade(self, percentage):
        if percentage is None:
            return "N/A"
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"

    def student_report(self, student_id):
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found")
        print(f"\n--- Report for {student.name} ---")
        courses = self.course_repo.get_all()
        for course in courses:
            avg = self.calculate_weighted_average(student_id, course.id)
            grade = self.letter_grade(avg)
            if avg is not None:
                print(f"{course.name}: Average {avg:.2f}% Grade {grade}")
            else:
                print(f"{course.name}: No graded assignments")
        print()