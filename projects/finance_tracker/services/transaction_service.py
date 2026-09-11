from datetime import datetime
from models.transaction import Transaction
from storage.transaction_repository import TransactionRepository
from storage.account_repository import AccountRepository
from storage.category_repository import CategoryRepository

class TransactionService:
    def __init__(self, db_path):
        self.tx_repo = TransactionRepository(db_path)
        self.account_repo = AccountRepository(db_path)
        self.category_repo = CategoryRepository(db_path)

    def _validate(self, account_id, category_id, type_, amount, date):
        if not self.account_repo.get_by_id(account_id):
            raise ValueError("Account not found.")
        if type_ not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not date or len(date) != 10:
            raise ValueError("Date must be in YYYY-MM-DD format.")
        if category_id:
            category = self.category_repo.get_by_id(category_id)
            if not category:
                raise ValueError("Category not found.")
            if category.type != type_:
                raise ValueError("Category type does not match transaction type.")

    def create_transaction(self, account_id, category_id, type_, amount, description, date):
        self._validate(account_id, category_id, type_, float(amount), date)
        tx = Transaction(
            account_id=account_id,
            category_id=category_id if category_id else None,
            type=type_,
            amount=float(amount),
            description=description.strip(),
            date=date,
            created_at=datetime.now().isoformat(timespec="seconds")
        )
        return self.tx_repo.insert(tx)

    def get_transaction(self, tx_id):
        return self.tx_repo.get_by_id(tx_id)

    def get_transactions(self, month=None, account_id=None, category_id=None, type_=None):
        return self.tx_repo.get_filtered(month, account_id, category_id, type_)

    def get_recent(self, limit=5):
        return self.tx_repo.get_recent(limit)

    def update_transaction(self, tx_id, account_id, category_id, type_, amount, description, date):
        tx = self.tx_repo.get_by_id(tx_id)
        if not tx:
            raise ValueError("Transaction not found.")
        self._validate(account_id, category_id, type_, float(amount), date)
        tx.account_id = account_id
        tx.category_id = category_id if category_id else None
        tx.type = type_
        tx.amount = float(amount)
        tx.description = description.strip()
        tx.date = date
        self.tx_repo.update(tx)
        return tx

    def delete_transaction(self, tx_id):
        if not self.tx_repo.get_by_id(tx_id):
            return False
        self.tx_repo.delete(tx_id)
        return True

    def monthly_summary(self, month):
        income, expense = self.tx_repo.sum_for_month(month)
        return {"income": income, "expense": expense, "net": income - expense}