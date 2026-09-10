import sqlite3
from models.question import Question

class QuestionRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, question):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO questions (quiz_id, text, position) VALUES (?, ?, ?)",
            (question.quiz_id, question.text, question.position)
        )
        conn.commit()
        question.id = cursor.lastrowid
        conn.close()
        return question

    def get_by_id(self, question_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Question(row["id"], row["quiz_id"], row["text"], row["position"])
        return None

    def get_by_quiz(self, quiz_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM questions WHERE quiz_id = ? ORDER BY position, id",
            (quiz_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [Question(r["id"], r["quiz_id"], r["text"], r["position"]) for r in rows]

    def update(self, question):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE questions SET text = ?, position = ? WHERE id = ?",
            (question.text, question.position, question.id)
        )
        conn.commit()
        conn.close()

    def delete(self, question_id):
        conn = self._connect()
        cursor = conn.cursor()
        # Delete associated options first
        cursor.execute("DELETE FROM options WHERE question_id = ?", (question_id,))
        cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()
        conn.close()

    def count_by_quiz(self, quiz_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS c FROM questions WHERE quiz_id = ?", (quiz_id,))
        row = cursor.fetchone()
        conn.close()
        return row["c"] if row else 0