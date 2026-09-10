class Attempt:
    def __init__(self, attempt_id=None, quiz_id=None, user_name="", score=0, total=0, taken_at=""):
        self.id = attempt_id
        self.quiz_id = quiz_id
        self.user_name = user_name
        self.score = score
        self.total = total
        self.taken_at = taken_at

    def __repr__(self):
        return f"Attempt(id={self.id}, user='{self.user_name}', score={self.score}/{self.total})"