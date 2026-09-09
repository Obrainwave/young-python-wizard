from models.course import Course
from storage.course_repository import CourseRepository

class CourseService:
    def __init__(self, db_path):
        self.repo = CourseRepository(db_path)

    def create_course(self, title, description="", credits=0):
        if not title.strip():
            raise ValueError("Course title cannot be empty.")
        if credits < 0:
            raise ValueError("Credits must be a non-negative number.")
        course = Course(title=title.strip(), description=description.strip(), credits=credits)
        return self.repo.insert(course)

    def get_course(self, course_id):
        return self.repo.get_by_id(course_id)

    def get_all_courses(self):
        return self.repo.get_all()

    def search_courses(self, term):
        return self.repo.search(term)

    def update_course(self, course_id, title, description="", credits=0):
        course = self.repo.get_by_id(course_id)
        if not course:
            raise ValueError("Course not found.")
        if not title.strip():
            raise ValueError("Course title cannot be empty.")
        if credits < 0:
            raise ValueError("Credits must be a non-negative number.")
        course.title = title.strip()
        course.description = description.strip()
        course.credits = credits
        self.repo.update(course)
        return course

    def delete_course(self, course_id):
        if not self.repo.get_by_id(course_id):
            return False
        self.repo.delete(course_id)
        return True