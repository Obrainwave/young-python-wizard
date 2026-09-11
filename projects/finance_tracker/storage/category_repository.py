import sqlite3
from models.category import Category

class CategoryRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, category):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name, type, color) VALUES (?, ?, ?)",
            (category.name, category.type, category.color)
        )
        conn.commit()
        category.id = cursor.lastrowid
        conn.close()
        return category

    def get_by_id(self, category_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_category(row) if row else None

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY type, name")
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_category(r) for r in rows]

    def get_by_type(self, ctype):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM categories WHERE type = ? ORDER BY name", (ctype,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_category(r) for r in rows]

    def update(self, category):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE categories SET name = ?, type = ?, color = ? WHERE id = ?",
            (category.name, category.type, category.color, category.id)
        )
        conn.commit()
        conn.close()

    def delete(self, category_id):
        conn = self._connect()
        cursor = conn.cursor()
        # Unlink transactions and remove budgets that reference this category
        cursor.execute("UPDATE transactions SET category_id = NULL WHERE category_id = ?", (category_id,))
        cursor.execute("DELETE FROM budgets WHERE category_id = ?", (category_id,))
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        conn.close()

    def _row_to_category(self, row):
        return Category(
            category_id=row["id"],
            name=row["name"],
            type=row["type"],
            color=row["color"]
        )