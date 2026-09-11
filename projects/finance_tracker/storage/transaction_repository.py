import sqlite3
from models.transaction import Transaction

class TransactionRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, tx):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (account_id, category_id, type, amount, description, date, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (tx.account_id, tx.category_id, tx.type, tx.amount,
             tx.description, tx.date, tx.created_at)
        )
        conn.commit()
        tx.id = cursor.lastrowid
        conn.close()
        return tx

    def get_by_id(self, tx_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_transaction(row) if row else None

    def get_filtered(self, month=None, account_id=None, category_id=None, type_=None):
        """
        Return transactions with joined account and category names for display.
        Returns raw sqlite3.Row objects to make joined fields easily accessible.
        """
        query = """
            SELECT t.id, t.account_id, t.category_id, t.type, t.amount,
                   t.description, t.date, t.created_at,
                   a.name AS account_name,
                   c.name AS category_name,
                   c.color AS category_color
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE 1 = 1
        """
        params = []
        if month:
            query += " AND substr(t.date, 1, 7) = ?"
            params.append(month)
        if account_id:
            query += " AND t.account_id = ?"
            params.append(account_id)
        if category_id:
            query += " AND t.category_id = ?"
            params.append(category_id)
        if type_:
            query += " AND t.type = ?"
            params.append(type_)
        query += " ORDER BY t.date DESC, t.id DESC"

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_recent(self, limit=5):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.account_id, t.category_id, t.type, t.amount,
                   t.description, t.date,
                   a.name AS account_name,
                   c.name AS category_name,
                   c.color AS category_color
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            LEFT JOIN categories c ON t.category_id = c.id
            ORDER BY t.date DESC, t.id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def update(self, tx):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE transactions SET account_id=?, category_id=?, type=?, amount=?, "
            "description=?, date=? WHERE id=?",
            (tx.account_id, tx.category_id, tx.type, tx.amount,
             tx.description, tx.date, tx.id)
        )
        conn.commit()
        conn.close()

    def delete(self, tx_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
        conn.commit()
        conn.close()

    def sum_by_account(self, account_id):
        """Return (total_income, total_expense) for the given account."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
              COALESCE(SUM(CASE WHEN type='income' THEN amount END), 0) AS income,
              COALESCE(SUM(CASE WHEN type='expense' THEN amount END), 0) AS expense
            FROM transactions WHERE account_id = ?
        """, (account_id,))
        row = cursor.fetchone()
        conn.close()
        return (row["income"], row["expense"]) if row else (0, 0)

    def sum_for_month(self, month):
        """Return (income, expense) totals for the given YYYY-MM month."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
              COALESCE(SUM(CASE WHEN type='income' THEN amount END), 0) AS income,
              COALESCE(SUM(CASE WHEN type='expense' THEN amount END), 0) AS expense
            FROM transactions WHERE substr(date, 1, 7) = ?
        """, (month,))
        row = cursor.fetchone()
        conn.close()
        return (row["income"], row["expense"]) if row else (0, 0)

    def sum_expense_by_category(self, category_id, month):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM transactions
            WHERE category_id = ? AND type = 'expense' AND substr(date, 1, 7) = ?
        """, (category_id, month))
        row = cursor.fetchone()
        conn.close()
        return row["total"] if row else 0

    def _row_to_transaction(self, row):
        return Transaction(
            transaction_id=row["id"],
            account_id=row["account_id"],
            category_id=row["category_id"],
            type=row["type"],
            amount=row["amount"],
            description=row["description"],
            date=row["date"],
            created_at=row["created_at"]
        )