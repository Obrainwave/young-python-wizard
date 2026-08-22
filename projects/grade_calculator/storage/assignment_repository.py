from models.assignment import Assignment

class AssignmentRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, assignment):
        self.db.execute(
            "INSERT INTO assignments (course_id, name, max_score, weight) VALUES (?, ?, ?, ?)",
            (assignment.course_id, assignment.name, assignment.max_score, assignment.weight)
        )
        self.db.commit()
        assignment.id = self.db.last_row_id()
        return assignment

    def get_by_id(self, assignment_id):
        self.db.execute("SELECT * FROM assignments WHERE id = ?", (assignment_id,))
        row = self.db.fetchone()
        if row:
            return Assignment(row["id"], row["course_id"], row["name"], row["max_score"], row["weight"])
        return None

    def get_by_course(self, course_id):
        self.db.execute("SELECT * FROM assignments WHERE course_id = ? ORDER BY id", (course_id,))
        rows = self.db.fetchall()
        return [Assignment(row["id"], row["course_id"], row["name"], row["max_score"], row["weight"]) for row in rows]

    def update(self, assignment):
        self.db.execute(
            "UPDATE assignments SET course_id=?, name=?, max_score=?, weight=? WHERE id=?",
            (assignment.course_id, assignment.name, assignment.max_score, assignment.weight, assignment.id)
        )
        self.db.commit()

    def delete(self, assignment_id):
        self.db.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
        self.db.commit()