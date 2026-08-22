from models.course import Course

class CourseRepository:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        self.db.commit()

    def insert(self, course):
        self.db.execute("INSERT INTO courses (name) VALUES (?)", (course.name,))
        self.db.commit()
        course.id = self.db.last_row_id()
        return course

    def get_by_id(self, course_id):
        self.db.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        row = self.db.fetchone()
        if row:
            return Course(row["id"], row["name"])
        return None

    def get_all(self):
        self.db.execute("SELECT * FROM courses ORDER BY name")
        rows = self.db.fetchall()
        return [Course(row["id"], row["name"]) for row in rows]

    def update(self, course):
        self.db.execute("UPDATE courses SET name = ? WHERE id = ?", (course.name, course.id))
        self.db.commit()

    def delete(self, course_id):
        self.db.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        self.db.commit()