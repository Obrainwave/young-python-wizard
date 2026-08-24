from models.expense import Expense

class ExpenseRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, expense):
        self.db.execute(
            "INSERT INTO expenses (category_id, amount, description, date) VALUES (?, ?, ?, ?)",
            (expense.category_id, expense.amount, expense.description, expense.date)
        )
        self.db.commit()
        expense.id = self.db.last_row_id()
        return expense

    def get_by_id(self, expense_id):
        self.db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        row = self.db.fetchone()
        if row:
            return self._row_to_expense(row)
        return None

    def get_all(self):
        self.db.execute("SELECT * FROM expenses ORDER BY date DESC")
        rows = self.db.fetchall()
        return [self._row_to_expense(row) for row in rows]

    def get_by_category(self, category_id):
        self.db.execute("SELECT * FROM expenses WHERE category_id = ? ORDER BY date DESC", (category_id,))
        rows = self.db.fetchall()
        return [self._row_to_expense(row) for row in rows]

    def get_by_date_range(self, start_date, end_date):
        self.db.execute(
            "SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC",
            (start_date, end_date)
        )
        rows = self.db.fetchall()
        return [self._row_to_expense(row) for row in rows]

    def update(self, expense):
        self.db.execute(
            "UPDATE expenses SET category_id = ?, amount = ?, description = ?, date = ? WHERE id = ?",
            (expense.category_id, expense.amount, expense.description, expense.date, expense.id)
        )
        self.db.commit()

    def delete(self, expense_id):
        self.db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.db.commit()

    def _row_to_expense(self, row):
        return Expense(
            expense_id=row["id"],
            category_id=row["category_id"],
            amount=row["amount"],
            description=row["description"],
            date=row["date"]
        )