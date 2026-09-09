import sqlite3
from models.course import Course

class CourseRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, course):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (title, description, credits) VALUES (?, ?, ?)",
            (course.title, course.description, course.credits)
        )
        conn.commit()
        course.id = cursor.lastrowid
        conn.close()
        return course

    def get_by_id(self, course_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return self._row_to_course(row)
        return None

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses ORDER BY title")
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_course(row) for row in rows]

    def search(self, term):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM courses WHERE title LIKE ? OR description LIKE ? ORDER BY title",
            (f"%{term}%", f"%{term}%")
        )
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_course(row) for row in rows]

    def update(self, course):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE courses SET title = ?, description = ?, credits = ? WHERE id = ?",
            (course.title, course.description, course.credits, course.id)
        )
        conn.commit()
        conn.close()

    def delete(self, course_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        conn.commit()
        conn.close()

    def _row_to_course(self, row):
        return Course(
            course_id=row["id"],
            title=row["title"],
            description=row["description"],
            credits=row["credits"]
        )