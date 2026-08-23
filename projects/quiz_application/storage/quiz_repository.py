from models.quiz import Quiz

class QuizRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, quiz):
        self.db.execute(
            "INSERT INTO quizzes (title, description) VALUES (?, ?)",
            (quiz.title, quiz.description)
        )
        self.db.commit()
        quiz.id = self.db.last_row_id()
        return quiz

    def get_by_id(self, quiz_id):
        self.db.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
        row = self.db.fetchone()
        if row:
            return Quiz(row["id"], row["title"], row["description"])
        return None

    def get_all(self):
        self.db.execute("SELECT * FROM quizzes ORDER BY title")
        rows = self.db.fetchall()
        return [Quiz(row["id"], row["title"], row["description"]) for row in rows]

    def update(self, quiz):
        self.db.execute(
            "UPDATE quizzes SET title = ?, description = ? WHERE id = ?",
            (quiz.title, quiz.description, quiz.id)
        )
        self.db.commit()

    def delete(self, quiz_id):
        self.db.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
        self.db.commit()