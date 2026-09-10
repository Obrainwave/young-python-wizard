import sqlite3
from models.quiz import Quiz

class QuizRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, quiz):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO quizzes (title, description, created_at) VALUES (?, ?, ?)",
            (quiz.title, quiz.description, quiz.created_at)
        )
        conn.commit()
        quiz.id = cursor.lastrowid
        conn.close()
        return quiz

    def get_by_id(self, quiz_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Quiz(row["id"], row["title"], row["description"], row["created_at"])
        return None

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quizzes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [Quiz(r["id"], r["title"], r["description"], r["created_at"]) for r in rows]

    def update(self, quiz):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE quizzes SET title = ?, description = ? WHERE id = ?",
            (quiz.title, quiz.description, quiz.id)
        )
        conn.commit()
        conn.close()

    def delete(self, quiz_id):
        conn = self._connect()
        cursor = conn.cursor()
        # Delete dependent rows manually since SQLite does not enforce cascade by default
        cursor.execute("""
            DELETE FROM attempt_answers WHERE attempt_id IN
            (SELECT id FROM attempts WHERE quiz_id = ?)
        """, (quiz_id,))
        cursor.execute("DELETE FROM attempts WHERE quiz_id = ?", (quiz_id,))
        cursor.execute("""
            DELETE FROM options WHERE question_id IN
            (SELECT id FROM questions WHERE quiz_id = ?)
        """, (quiz_id,))
        cursor.execute("DELETE FROM questions WHERE quiz_id = ?", (quiz_id,))
        cursor.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
        conn.commit()
        conn.close()