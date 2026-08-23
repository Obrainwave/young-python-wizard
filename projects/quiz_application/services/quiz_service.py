import json
from datetime import datetime
from models.quiz import Quiz
from models.question import Question
from models.quiz_result import QuizResult
from storage.quiz_repository import QuizRepository
from storage.question_repository import QuestionRepository
from storage.result_repository import ResultRepository

class QuizService:
    def __init__(self, db):
        self.quiz_repo = QuizRepository(db)
        self.question_repo = QuestionRepository(db)
        self.result_repo = ResultRepository(db)

    # Quiz operations
    def create_quiz(self, title, description=""):
        quiz = Quiz(title=title, description=description)
        return self.quiz_repo.insert(quiz)

    def get_all_quizzes(self):
        return self.quiz_repo.get_all()

    def get_quiz(self, quiz_id):
        return self.quiz_repo.get_by_id(quiz_id)

    def delete_quiz(self, quiz_id):
        # Also delete related questions and results
        questions = self.question_repo.get_by_quiz(quiz_id)
        for q in questions:
            self.question_repo.delete(q.id)
        # Delete results (no method yet, but could add)
        # For now, just delete quiz; foreign key cascade could be set up, but we'll keep simple
        self.quiz_repo.delete(quiz_id)

    # Question operations
    def add_question(self, quiz_id, text, options, correct_index):
        if len(options) < 2:
            raise ValueError("At least two options are required.")
        if correct_index < 0 or correct_index >= len(options):
            raise ValueError("Correct index is out of range.")
        question = Question(quiz_id=quiz_id, text=text, options=options, correct_index=correct_index)
        return self.question_repo.insert(question)

    def get_questions_for_quiz(self, quiz_id):
        return self.question_repo.get_by_quiz(quiz_id)

    # Quiz taking
    def take_quiz(self, quiz_id):
        quiz = self.quiz_repo.get_by_id(quiz_id)
        if not quiz:
            raise ValueError("Quiz not found.")
        questions = self.question_repo.get_by_quiz(quiz_id)
        if not questions:
            raise ValueError("This quiz has no questions.")

        score = 0
        total = len(questions)
        for i, question in enumerate(questions, start=1):
            print(f"\nQuestion {i}/{total}: {question.text}")
            for j, option in enumerate(question.options):
                print(f"  {j + 1}. {option}")
            while True:
                try:
                    answer = int(input("Your answer (1-{}): ".format(len(question.options))))
                    if 1 <= answer <= len(question.options):
                        break
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Please enter a number.")
            if answer - 1 == question.correct_index:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong. The correct answer was {question.correct_index + 1}.")

        # Save result
        result = QuizResult(
            quiz_id=quiz_id,
            score=score,
            total_questions=total,
            taken_at=datetime.now().isoformat(timespec='seconds')
        )
        self.result_repo.insert(result)

        print(f"\nQuiz completed! Your score: {score}/{total}")
        return result

    def get_results_for_quiz(self, quiz_id):
        return self.result_repo.get_by_quiz(quiz_id)