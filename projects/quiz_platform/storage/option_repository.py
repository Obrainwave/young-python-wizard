import sqlite3
from models.option import Option

class OptionRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, option):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO options (question_id, text, is_correct) VALUES (?, ?, ?)",
            (option.question_id, option.text, 1 if option.is_correct else 0)
        )
        conn.commit()
        option.id = cursor.lastrowid
        conn.close()
        return option

    def get_by_question(self, question_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM options WHERE question_id = ? ORDER BY id", (question_id,))
        rows = cursor.fetchall()
        conn.close()
        return [
            Option(r["id"], r["question_id"], r["text"], bool(r["is_correct"]))
            for r in rows
        ]

    def delete_by_question(self, question_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM options WHERE question_id = ?", (question_id,))
        conn.commit()
        conn.close()