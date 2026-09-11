import sqlite3
from models.budget import Budget

class BudgetRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def upsert(self, budget):
        """Insert or update budget for (category_id, month)."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO budgets (category_id, month, amount)
            VALUES (?, ?, ?)
            ON CONFLICT(category_id, month) DO UPDATE SET amount = excluded.amount
        """, (budget.category_id, budget.month, budget.amount))
        conn.commit()
        # Fetch id for the inserted/updated row
        cursor.execute(
            "SELECT id FROM budgets WHERE category_id = ? AND month = ?",
            (budget.category_id, budget.month)
        )
        row = cursor.fetchone()
        budget.id = row["id"] if row else None
        conn.close()
        return budget

    def get_by_id(self, budget_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM budgets WHERE id = ?", (budget_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_budget(row) if row else None

    def get_for_month(self, month):
        """Return list of dicts: budget, category, spent, progress."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, b.category_id, b.month, b.amount,
                   c.name AS category_name, c.color AS category_color
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            WHERE b.month = ?
            ORDER BY c.name
        """, (month,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete(self, budget_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
        conn.commit()
        conn.close()

    def _row_to_budget(self, row):
        return Budget(
            budget_id=row["id"],
            category_id=row["category_id"],
            month=row["month"],
            amount=row["amount"]
        )