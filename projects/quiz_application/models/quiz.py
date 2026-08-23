class Quiz:
    def __init__(self, quiz_id=None, title="", description=""):
        self.id = quiz_id
        self.title = title
        self.description = description

    def __repr__(self):
        return f"Quiz(id={self.id}, title='{self.title}', description='{self.description}')"