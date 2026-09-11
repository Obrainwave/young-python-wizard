from models.budget import Budget
from storage.budget_repository import BudgetRepository
from storage.category_repository import CategoryRepository
from storage.transaction_repository import TransactionRepository

class BudgetService:
    def __init__(self, db_path):
        self.repo = BudgetRepository(db_path)
        self.category_repo = CategoryRepository(db_path)
        self.tx_repo = TransactionRepository(db_path)

    def set_budget(self, category_id, month, amount):
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found.")
        if category.type != "expense":
            raise ValueError("Budgets can only be set for expense categories.")
        if amount <= 0:
            raise ValueError("Budget amount must be greater than zero.")
        budget = Budget(category_id=category_id, month=month, amount=float(amount))
        return self.repo.upsert(budget)

    def get_budget(self, budget_id):
        return self.repo.get_by_id(budget_id)

    def get_budgets_with_progress(self, month):
        """
        Return list of dicts with category, budget amount, amount spent,
        percent used, and remaining.
        """
        rows = self.repo.get_for_month(month)
        result = []
        for r in rows:
            spent = self.tx_repo.sum_expense_by_category(r["category_id"], month)
            amount = r["amount"]
            percent = (spent / amount * 100) if amount > 0 else 0
            remaining = amount - spent
            result.append({
                "id": r["id"],
                "category_id": r["category_id"],
                "category_name": r["category_name"],
                "category_color": r["category_color"],
                "budget": amount,
                "spent": spent,
                "remaining": remaining,
                "percent": round(percent, 1)
            })
        return result

    def delete_budget(self, budget_id):
        if not self.repo.get_by_id(budget_id):
            return False
        self.repo.delete(budget_id)
        return True