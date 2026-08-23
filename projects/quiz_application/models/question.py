class Question:
    def __init__(self, question_id=None, quiz_id=None, text="", options=None, correct_index=0):
        self.id = question_id
        self.quiz_id = quiz_id
        self.text = text
        self.options = options if options is not None else []
        self.correct_index = correct_index

    def __repr__(self):
        return (f"Question(id={self.id}, quiz_id={self.quiz_id}, "
                f"text='{self.text}', options={self.options}, correct_index={self.correct_index})")