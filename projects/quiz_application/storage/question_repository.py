import json
from models.question import Question

class QuestionRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, question):
        options_json = json.dumps(question.options)
        self.db.execute(
            "INSERT INTO questions (quiz_id, text, options, correct_index) VALUES (?, ?, ?, ?)",
            (question.quiz_id, question.text, options_json, question.correct_index)
        )
        self.db.commit()
        question.id = self.db.last_row_id()
        return question

    def get_by_id(self, question_id):
        self.db.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
        row = self.db.fetchone()
        if row:
            return self._row_to_question(row)
        return None

    def get_by_quiz(self, quiz_id):
        self.db.execute("SELECT * FROM questions WHERE quiz_id = ? ORDER BY id", (quiz_id,))
        rows = self.db.fetchall()
        return [self._row_to_question(row) for row in rows]

    def update(self, question):
        options_json = json.dumps(question.options)
        self.db.execute(
            "UPDATE questions SET quiz_id = ?, text = ?, options = ?, correct_index = ? WHERE id = ?",
            (question.quiz_id, question.text, options_json, question.correct_index, question.id)
        )
        self.db.commit()

    def delete(self, question_id):
        self.db.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        self.db.commit()

    def _row_to_question(self, row):
        return Question(
            question_id=row["id"],
            quiz_id=row["quiz_id"],
            text=row["text"],
            options=json.loads(row["options"]),
            correct_index=row["correct_index"]
        )