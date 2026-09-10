from datetime import datetime
from models.attempt import Attempt
from storage.attempt_repository import AttemptRepository
from storage.question_repository import QuestionRepository
from storage.option_repository import OptionRepository


class AttemptService:
    def __init__(self, db_path):
        self.attempt_repo = AttemptRepository(db_path)
        self.question_repo = QuestionRepository(db_path)
        self.option_repo = OptionRepository(db_path)

    def submit_attempt(self, quiz_id, user_name, answers):
        """
        answers: dict {question_id (int): option_id (int)}
        Returns the saved Attempt object.
        """
        if not user_name.strip():
            raise ValueError("Please enter your name.")
        questions = self.question_repo.get_by_quiz(quiz_id)
        if not questions:
            raise ValueError("This quiz has no questions yet.")

        score = 0
        stored_answers = []

        for q in questions:
            chosen_option_id = answers.get(q.id)
            if chosen_option_id is None:
                # Unanswered question counts as wrong.
                stored_answers.append((q.id, None))
                continue

            # Verify that the chosen option belongs to this question.
            options = self.option_repo.get_by_question(q.id)
            chosen = next((o for o in options if o.id == chosen_option_id), None)
            if chosen is None:
                stored_answers.append((q.id, None))
                continue

            if chosen.is_correct:
                score += 1
            stored_answers.append((q.id, chosen.id))

        attempt = Attempt(
            quiz_id=quiz_id,
            user_name=user_name.strip(),
            score=score,
            total=len(questions),
            taken_at=datetime.now().isoformat(timespec="seconds")
        )
        return self.attempt_repo.insert(attempt, stored_answers)

    def get_attempt(self, attempt_id):
        return self.attempt_repo.get_by_id(attempt_id)

    def get_leaderboard(self, quiz_id, limit=10):
        return self.attempt_repo.get_by_quiz(quiz_id, limit=limit)

    def get_detailed_results(self, attempt_id, quiz_service):
        """
        Return a list of dicts describing each question: text, chosen option,
        correct option, and whether the answer was correct.
        """
        attempt = self.attempt_repo.get_by_id(attempt_id)
        if not attempt:
            return None, []
        answers = dict(self.attempt_repo.get_answers(attempt_id))
        questions = quiz_service.get_questions_for_quiz(attempt.quiz_id)
        details = []
        for q in questions:
            chosen_id = answers.get(q.id)
            chosen = next((o for o in q.options if o.id == chosen_id), None)
            correct = next((o for o in q.options if o.is_correct), None)
            details.append({
                "question": q,
                "chosen": chosen,
                "correct": correct,
                "is_correct": bool(chosen and chosen.is_correct),
            })
        return attempt, details