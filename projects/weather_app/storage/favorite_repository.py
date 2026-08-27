from models.favorite import FavoriteCity

class FavoriteRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, favorite):
        self.db.execute(
            "INSERT INTO favorites (city, latitude, longitude, added_at) VALUES (?, ?, ?, ?)",
            (favorite.city, favorite.latitude, favorite.longitude, favorite.added_at)
        )
        self.db.commit()
        favorite.id = self.db.last_row_id()
        return favorite

    def get_all(self):
        self.db.execute("SELECT * FROM favorites ORDER BY city")
        rows = self.db.fetchall()
        return [
            FavoriteCity(
                id=row["id"],
                city=row["city"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                added_at=row["added_at"]
            )
            for row in rows
        ]

    def get_by_city(self, city):
        self.db.execute("SELECT * FROM favorites WHERE city = ?", (city,))
        row = self.db.fetchone()
        if row:
            return FavoriteCity(
                id=row["id"],
                city=row["city"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                added_at=row["added_at"]
            )
        return None

    def delete(self, city_id):
        self.db.execute("DELETE FROM favorites WHERE id = ?", (city_id,))
        self.db.commit()