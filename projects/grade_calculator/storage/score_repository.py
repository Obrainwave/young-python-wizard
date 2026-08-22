class ScoreRepository:
    def __init__(self, db):
        self.db = db

    def upsert_score(self, student_id, assignment_id, score):
        """Insert or update a score for a student on an assignment."""
        self.db.execute("""
            INSERT INTO scores (student_id, assignment_id, score)
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, assignment_id) DO UPDATE SET score=excluded.score
        """, (student_id, assignment_id, score))
        self.db.commit()

    def get_score(self, student_id, assignment_id):
        self.db.execute(
            "SELECT score FROM scores WHERE student_id=? AND assignment_id=?",
            (student_id, assignment_id)
        )
        row = self.db.fetchone()
        return row["score"] if row else None

    def delete_by_student(self, student_id):
        self.db.execute("DELETE FROM scores WHERE student_id = ?", (student_id,))
        self.db.commit()

    def delete_by_assignment(self, assignment_id):
        self.db.execute("DELETE FROM scores WHERE assignment_id = ?", (assignment_id,))
        self.db.commit()