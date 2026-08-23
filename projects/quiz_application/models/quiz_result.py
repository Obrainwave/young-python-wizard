class QuizResult:
    def __init__(self, result_id=None, quiz_id=None, score=0, total_questions=0, taken_at=""):
        self.id = result_id
        self.quiz_id = quiz_id
        self.score = score
        self.total_questions = total_questions
        self.taken_at = taken_at

    def __repr__(self):
        return (f"QuizResult(id={self.id}, quiz_id={self.quiz_id}, "
                f"score={self.score}, total_questions={self.total_questions}, taken_at='{self.taken_at}')")