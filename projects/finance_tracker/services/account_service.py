from datetime import datetime
from models.account import Account
from storage.account_repository import AccountRepository
from storage.transaction_repository import TransactionRepository

class AccountService:
    def __init__(self, db_path):
        self.repo = AccountRepository(db_path)
        self.tx_repo = TransactionRepository(db_path)

    def create_account(self, name, account_type, initial_balance=0.0, currency="USD"):
        if not name.strip():
            raise ValueError("Account name cannot be empty.")
        if account_type not in ("checking", "savings", "cash", "credit"):
            raise ValueError("Invalid account type.")
        account = Account(
            name=name.strip(),
            account_type=account_type,
            initial_balance=float(initial_balance),
            currency=currency.strip() or "USD",
            created_at=datetime.now().isoformat(timespec="seconds")
        )
        return self.repo.insert(account)

    def get_account(self, account_id):
        return self.repo.get_by_id(account_id)

    def get_all_accounts(self):
        return self.repo.get_all()

    def get_account_balance(self, account_id):
        """Return current balance = initial + income - expense."""
        account = self.repo.get_by_id(account_id)
        if not account:
            return 0.0
        income, expense = self.tx_repo.sum_by_account(account_id)
        return account.initial_balance + income - expense

    def get_all_with_balances(self):
        """Return list of dicts: account, current_balance."""
        result = []
        for acc in self.repo.get_all():
            income, expense = self.tx_repo.sum_by_account(acc.id)
            balance = acc.initial_balance + income - expense
            result.append({"account": acc, "balance": balance})
        return result

    def get_total_balance(self):
        """Sum of current balances across all accounts."""
        total = 0.0
        for acc in self.repo.get_all():
            income, expense = self.tx_repo.sum_by_account(acc.id)
            total += acc.initial_balance + income - expense
        return total

    def update_account(self, account_id, name, account_type, initial_balance, currency="USD"):
        account = self.repo.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found.")
        if not name.strip():
            raise ValueError("Account name cannot be empty.")
        if account_type not in ("checking", "savings", "cash", "credit"):
            raise ValueError("Invalid account type.")
        account.name = name.strip()
        account.account_type = account_type
        account.initial_balance = float(initial_balance)
        account.currency = currency.strip() or "USD"
        self.repo.update(account)
        return account

    def delete_account(self, account_id):
        if not self.repo.get_by_id(account_id):
            return False
        self.repo.delete(account_id)
        return True