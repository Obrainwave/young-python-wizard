class Quiz:
    def __init__(self, quiz_id=None, title="", description="", created_at=""):
        self.id = quiz_id
        self.title = title
        self.description = description
        self.created_at = created_at

    def __repr__(self):
        return f"Quiz(id={self.id}, title='{self.title}')"