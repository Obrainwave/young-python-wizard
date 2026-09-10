class Question:
    def __init__(self, question_id=None, quiz_id=None, text="", position=0, options=None):
        self.id = question_id
        self.quiz_id = quiz_id
        self.text = text
        self.position = position
        self.options = options if options is not None else []

    def __repr__(self):
        return f"Question(id={self.id}, quiz_id={self.quiz_id}, text='{self.text[:30]}...')"