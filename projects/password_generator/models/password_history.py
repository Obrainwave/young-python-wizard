class PasswordHistory:
    def __init__(self, id=None, password="", length=0, char_types="", created_at=""):
        self.id = id
        self.password = password
        self.length = length
        self.char_types = char_types
        self.created_at = created_at

    def __repr__(self):
        return (f"PasswordHistory(id={self.id}, password='{self.password}', "
                f"length={self.length}, char_types='{self.char_types}', "
                f"created_at='{self.created_at}')")