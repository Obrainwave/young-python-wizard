import sqlite3
from models.account import Account

class AccountRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, account):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts (name, account_type, initial_balance, currency, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (account.name, account.account_type, account.initial_balance,
             account.currency, account.created_at)
        )
        conn.commit()
        account.id = cursor.lastrowid
        conn.close()
        return account

    def get_by_id(self, account_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_account(row) if row else None

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_account(r) for r in rows]

    def update(self, account):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET name = ?, account_type = ?, initial_balance = ?, currency = ? "
            "WHERE id = ?",
            (account.name, account.account_type, account.initial_balance,
             account.currency, account.id)
        )
        conn.commit()
        conn.close()

    def delete(self, account_id):
        conn = self._connect()
        cursor = conn.cursor()
        # Delete transactions for this account first
        cursor.execute("DELETE FROM transactions WHERE account_id = ?", (account_id,))
        cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        conn.commit()
        conn.close()

    def _row_to_account(self, row):
        return Account(
            account_id=row["id"],
            name=row["name"],
            account_type=row["account_type"],
            initial_balance=row["initial_balance"],
            currency=row["currency"],
            created_at=row["created_at"]
        )