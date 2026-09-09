import sqlite3
from models.student import Student

class StudentRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, student):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, phone) VALUES (?, ?, ?)",
            (student.name, student.email, student.phone)
        )
        conn.commit()
        student.id = cursor.lastrowid
        conn.close()
        return student

    def get_by_id(self, student_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return self._row_to_student(row)
        return None

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_student(row) for row in rows]

    def search(self, term):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE ? OR email LIKE ? ORDER BY name",
            (f"%{term}%", f"%{term}%")
        )
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_student(row) for row in rows]

    def update(self, student):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET name = ?, email = ?, phone = ? WHERE id = ?",
            (student.name, student.email, student.phone, student.id)
        )
        conn.commit()
        conn.close()

    def delete(self, student_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()

    def _row_to_student(self, row):
        return Student(
            student_id=row["id"],
            name=row["name"],
            email=row["email"],
            phone=row["phone"]
        )