class Member:
    def __init__(self, member_id=None, name="", email=""):
        self.id = member_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Member(id={self.id}, name='{self.name}', email='{self.email}')"