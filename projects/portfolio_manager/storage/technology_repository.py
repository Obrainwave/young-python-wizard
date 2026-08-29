from models.technology import Technology

class TechnologyRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        self.db.execute("SELECT * FROM technologies ORDER BY name")
        rows = self.db.fetchall()
        return [Technology(row["id"], row["name"]) for row in rows]

    def get_by_name(self, name):
        self.db.execute("SELECT * FROM technologies WHERE name = ?", (name,))
        row = self.db.fetchone()
        if row:
            return Technology(row["id"], row["name"])
        return None