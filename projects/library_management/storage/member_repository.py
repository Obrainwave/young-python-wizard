from models.member import Member

class MemberRepository:
    def __init__(self, db):
        self.db = db
        
    def insert(self, member):
        self.db.execute(
            "INSERT INTO members (name, email) VALUES (?, ?)",
                (member.name, member.email)
        )
        self.db.commit()
        member.id = self.db.last_row_id()
        return member