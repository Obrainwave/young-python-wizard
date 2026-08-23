from models.quiz_result import QuizResult

class ResultRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, result):
        self.db.execute(
            "INSERT INTO results (quiz_id, score, total_questions, taken_at) VALUES (?, ?, ?, ?)",
            (result.quiz_id, result.score, result.total_questions, result.taken_at)
        )
        self.db.commit()
        result.id = self.db.last_row_id()
        return result

    def get_by_quiz(self, quiz_id):
        self.db.execute("SELECT * FROM results WHERE quiz_id = ? ORDER BY taken_at DESC", (quiz_id,))
        rows = self.db.fetchall()
        return [
            QuizResult(
                result_id=row["id"],
                quiz_id=row["quiz_id"],
                score=row["score"],
                total_questions=row["total_questions"],
                taken_at=row["taken_at"]
            )
            for row in rows
        ]

    def get_all(self):
        self.db.execute("SELECT * FROM results ORDER BY taken_at DESC")
        rows = self.db.fetchall()
        return [
            QuizResult(
                result_id=row["id"],
                quiz_id=row["quiz_id"],
                score=row["score"],
                total_questions=row["total_questions"],
                taken_at=row["taken_at"]
            )
            for row in rows
        ]