from models.password_history import PasswordHistory

class PasswordHistoryRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, entry):
        self.db.execute(
            "INSERT INTO password_history (password, length, char_types, created_at) "
            "VALUES (?, ?, ?, ?)",
            (entry.password, entry.length, entry.char_types, entry.created_at)
        )
        self.db.commit()
        entry.id = self.db.last_row_id()
        return entry

    def get_all(self):
        self.db.execute("SELECT * FROM password_history ORDER BY id DESC")
        rows = self.db.fetchall()
        return [
            PasswordHistory(
                id=row["id"],
                password=row["password"],
                length=row["length"],
                char_types=row["char_types"],
                created_at=row["created_at"]
            )
            for row in rows
        ]

    def delete_all(self):
        self.db.execute("DELETE FROM password_history")
        self.db.commit()