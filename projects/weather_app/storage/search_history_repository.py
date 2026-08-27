from models.search_history import SearchHistory

class SearchHistoryRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, entry):
        self.db.execute(
            "INSERT INTO search_history (city, temperature, windspeed, searched_at) VALUES (?, ?, ?, ?)",
            (entry.city, entry.temperature, entry.windspeed, entry.searched_at)
        )
        self.db.commit()
        entry.id = self.db.last_row_id()
        return entry

    def get_all(self):
        self.db.execute("SELECT * FROM search_history ORDER BY searched_at DESC LIMIT 50")
        rows = self.db.fetchall()
        return [
            SearchHistory(
                id=row["id"],
                city=row["city"],
                temperature=row["temperature"],
                windspeed=row["windspeed"],
                searched_at=row["searched_at"]
            )
            for row in rows
        ]

    def delete_all(self):
        self.db.execute("DELETE FROM search_history")
        self.db.commit()