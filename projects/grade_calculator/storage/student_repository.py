from models.student import Student

class StudentRepository:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        self.db.commit()

    def insert(self, student):
        self.db.execute(
            "INSERT INTO students (name) VALUES (?)",
            (student.name,)
        )
        self.db.commit()
        student.id = self.db.last_row_id()
        return student

    def get_by_id(self, student_id):
        self.db.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = self.db.fetchone()
        if row:
            return Student(row["id"], row["name"])
        return None

    def get_all(self):
        self.db.execute("SELECT * FROM students ORDER BY name")
        rows = self.db.fetchall()
        return [Student(row["id"], row["name"]) for row in rows]

    def update(self, student):
        self.db.execute(
            "UPDATE students SET name = ? WHERE id = ?",
            (student.name, student.id)
        )
        self.db.commit()

    def delete(self, student_id):
        self.db.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.db.commit()