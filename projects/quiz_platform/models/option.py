class Option:
    def __init__(self, option_id=None, question_id=None, text="", is_correct=False):
        self.id = option_id
        self.question_id = question_id
        self.text = text
        self.is_correct = is_correct

    def __repr__(self):
        return f"Option(id={self.id}, text='{self.text}', correct={self.is_correct})"