from datetime import datetime
from models.quiz import Quiz
from models.question import Question
from models.option import Option
from storage.quiz_repository import QuizRepository
from storage.question_repository import QuestionRepository
from storage.option_repository import OptionRepository


class QuizService:
    def __init__(self, db_path):
        self.quiz_repo = QuizRepository(db_path)
        self.question_repo = QuestionRepository(db_path)
        self.option_repo = OptionRepository(db_path)

    # ---------- Quiz operations ----------
    def create_quiz(self, title, description=""):
        if not title.strip():
            raise ValueError("Quiz title cannot be empty.")
        quiz = Quiz(
            title=title.strip(),
            description=description.strip(),
            created_at=datetime.now().isoformat(timespec="seconds")
        )
        return self.quiz_repo.insert(quiz)

    def get_quiz(self, quiz_id):
        return self.quiz_repo.get_by_id(quiz_id)

    def get_all_quizzes(self):
        return self.quiz_repo.get_all()

    def update_quiz(self, quiz_id, title, description=""):
        quiz = self.quiz_repo.get_by_id(quiz_id)
        if not quiz:
            raise ValueError("Quiz not found.")
        if not title.strip():
            raise ValueError("Quiz title cannot be empty.")
        quiz.title = title.strip()
        quiz.description = description.strip()
        self.quiz_repo.update(quiz)
        return quiz

    def delete_quiz(self, quiz_id):
        if not self.quiz_repo.get_by_id(quiz_id):
            return False
        self.quiz_repo.delete(quiz_id)
        return True

    # ---------- Question operations ----------
    def add_question(self, quiz_id, text, options, correct_index):
        """
        options: list of 4 strings
        correct_index: index (0-3) of the correct option
        """
        if not self.quiz_repo.get_by_id(quiz_id):
            raise ValueError("Quiz not found.")
        if not text.strip():
            raise ValueError("Question text cannot be empty.")
        if len(options) != 4 or any(not o.strip() for o in options):
            raise ValueError("You must provide 4 non-empty options.")
        if correct_index not in (0, 1, 2, 3):
            raise ValueError("Correct index must be between 0 and 3.")

        # Determine position
        position = self.question_repo.count_by_quiz(quiz_id) + 1
        question = self.question_repo.insert(
            Question(quiz_id=quiz_id, text=text.strip(), position=position)
        )
        for i, opt_text in enumerate(options):
            self.option_repo.insert(
                Option(question_id=question.id, text=opt_text.strip(),
                       is_correct=(i == correct_index))
            )
        return question

    def get_questions_for_quiz(self, quiz_id):
        """Return questions with their options attached."""
        questions = self.question_repo.get_by_quiz(quiz_id)
        for q in questions:
            q.options = self.option_repo.get_by_question(q.id)
        return questions

    def get_question(self, question_id):
        q = self.question_repo.get_by_id(question_id)
        if q:
            q.options = self.option_repo.get_by_question(q.id)
        return q

    def update_question(self, question_id, text, options, correct_index):
        q = self.question_repo.get_by_id(question_id)
        if not q:
            raise ValueError("Question not found.")
        if not text.strip():
            raise ValueError("Question text cannot be empty.")
        if len(options) != 4 or any(not o.strip() for o in options):
            raise ValueError("You must provide 4 non-empty options.")
        if correct_index not in (0, 1, 2, 3):
            raise ValueError("Correct index must be between 0 and 3.")

        q.text = text.strip()
        self.question_repo.update(q)

        # Replace all options (simplest and safest)
        self.option_repo.delete_by_question(question_id)
        for i, opt_text in enumerate(options):
            self.option_repo.insert(
                Option(question_id=question_id, text=opt_text.strip(),
                       is_correct=(i == correct_index))
            )
        return q

    def delete_question(self, question_id):
        if not self.question_repo.get_by_id(question_id):
            return False
        self.question_repo.delete(question_id)
        return True

    def count_questions(self, quiz_id):
        return self.question_repo.count_by_quiz(quiz_id)