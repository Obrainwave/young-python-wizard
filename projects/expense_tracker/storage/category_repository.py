from models.category import Category

class CategoryRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, category):
        self.db.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (category.name,)
        )
        self.db.commit()
        category.id = self.db.last_row_id()
        return category

    def get_by_id(self, category_id):
        self.db.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = self.db.fetchone()
        if row:
            return Category(row["id"], row["name"])
        return None

    def get_all(self):
        self.db.execute("SELECT * FROM categories ORDER BY name")
        rows = self.db.fetchall()
        return [Category(row["id"], row["name"]) for row in rows]

    def delete(self, category_id):
        self.db.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.db.commit()