import sqlite3
from models.attempt import Attempt

class AttemptRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, attempt, answers):
        """
        Insert an attempt along with its answers.
        answers: list of (question_id, option_id) tuples.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO attempts (quiz_id, user_name, score, total, taken_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (attempt.quiz_id, attempt.user_name, attempt.score,
             attempt.total, attempt.taken_at)
        )
        attempt.id = cursor.lastrowid
        for qid, oid in answers:
            cursor.execute(
                "INSERT INTO attempt_answers (attempt_id, question_id, option_id) "
                "VALUES (?, ?, ?)",
                (attempt.id, qid, oid)
            )
        conn.commit()
        conn.close()
        return attempt

    def get_by_id(self, attempt_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM attempts WHERE id = ?", (attempt_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Attempt(row["id"], row["quiz_id"], row["user_name"],
                           row["score"], row["total"], row["taken_at"])
        return None

    def get_by_quiz(self, quiz_id, limit=None):
        conn = self._connect()
        cursor = conn.cursor()
        query = "SELECT * FROM attempts WHERE quiz_id = ? ORDER BY score DESC, taken_at ASC"
        if limit:
            query += f" LIMIT {int(limit)}"
        cursor.execute(query, (quiz_id,))
        rows = cursor.fetchall()
        conn.close()
        return [
            Attempt(r["id"], r["quiz_id"], r["user_name"],
                    r["score"], r["total"], r["taken_at"])
            for r in rows
        ]

    def get_answers(self, attempt_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT question_id, option_id FROM attempt_answers WHERE attempt_id = ?",
            (attempt_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [(r["question_id"], r["option_id"]) for r in rows]