import sqlite3
from models.enrollment import Enrollment

class EnrollmentRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, enrollment):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO enrollments (student_id, course_id, grade, enrolled_on) VALUES (?, ?, ?, ?)",
            (enrollment.student_id, enrollment.course_id, enrollment.grade, enrollment.enrolled_on)
        )
        conn.commit()
        enrollment.id = cursor.lastrowid
        conn.close()
        return enrollment

    def get_by_id(self, enrollment_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.student_id, e.course_id, e.grade, e.enrolled_on,
                   s.name AS student_name, c.title AS course_title
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            JOIN courses c ON e.course_id = c.id
            WHERE e.id = ?
        """, (enrollment_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row
        return None

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.student_id, e.course_id, e.grade, e.enrolled_on,
                   s.name AS student_name, c.title AS course_title
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            JOIN courses c ON e.course_id = c.id
            ORDER BY e.enrolled_on DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_by_student(self, student_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.student_id, e.course_id, e.grade, e.enrolled_on,
                   s.name AS student_name, c.title AS course_title
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            JOIN courses c ON e.course_id = c.id
            WHERE e.student_id = ?
            ORDER BY e.enrolled_on DESC
        """, (student_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_by_course(self, course_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.student_id, e.course_id, e.grade, e.enrolled_on,
                   s.name AS student_name, c.title AS course_title
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            JOIN courses c ON e.course_id = c.id
            WHERE e.course_id = ?
            ORDER BY e.enrolled_on DESC
        """, (course_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_raw_by_id(self, enrollment_id):
        """Fetch enrollment as a model object for editing."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM enrollments WHERE id = ?", (enrollment_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return self._row_to_enrollment(row)
        return None

    def update(self, enrollment):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE enrollments SET student_id=?, course_id=?, grade=?, enrolled_on=? WHERE id=?",
            (enrollment.student_id, enrollment.course_id, enrollment.grade,
             enrollment.enrolled_on, enrollment.id)
        )
        conn.commit()
        conn.close()

    def delete(self, enrollment_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM enrollments WHERE id = ?", (enrollment_id,))
        conn.commit()
        conn.close()

    def _row_to_enrollment(self, row):
        return Enrollment(
            enrollment_id=row["id"],
            student_id=row["student_id"],
            course_id=row["course_id"],
            grade=row["grade"],
            enrolled_on=row["enrolled_on"]
        )