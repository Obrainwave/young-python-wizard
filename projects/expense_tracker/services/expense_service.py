from datetime import date, datetime
from models.category import Category
from models.expense import Expense
from storage.category_repository import CategoryRepository
from storage.expense_repository import ExpenseRepository

class ExpenseService:
    def __init__(self, db):
        self.category_repo = CategoryRepository(db)
        self.expense_repo = ExpenseRepository(db)

    # Category operations
    def add_category(self, name):
        if not name.strip():
            raise ValueError("Category name cannot be empty.")
        name = name.strip()
        # Optionally check for duplicates
        for cat in self.category_repo.get_all():
            if cat.name.lower() == name.lower():
                raise ValueError("Category already exists.")
        category = Category(name=name)
        return self.category_repo.insert(category)

    def get_all_categories(self):
        return self.category_repo.get_all()

    def delete_category(self, category_id):
        # Check if there are expenses associated
        expenses = self.expense_repo.get_by_category(category_id)
        if expenses:
            raise ValueError("Cannot delete category with existing expenses.")
        self.category_repo.delete(category_id)

    # Expense operations
    def add_expense(self, category_id, amount, description="", date_str=None):
        # Validate category exists
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if date_str is None:
            date_str = date.today().isoformat()
        else:
            # Validate date format
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format.")
        expense = Expense(
            category_id=category_id,
            amount=amount,
            description=description.strip(),
            date=date_str
        )
        return self.expense_repo.insert(expense)

    def get_all_expenses(self):
        return self.expense_repo.get_all()

    def get_expenses_by_category(self, category_id):
        return self.expense_repo.get_by_category(category_id)

    def get_expenses_by_date_range(self, start_date, end_date):
        return self.expense_repo.get_by_date_range(start_date, end_date)

    def update_expense(self, expense_id, category_id, amount, description, date_str):
        expense = self.expense_repo.get_by_id(expense_id)
        if not expense:
            raise ValueError("Expense not found.")
        # Validate as in add
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        expense.category_id = category_id
        expense.amount = amount
        expense.description = description.strip()
        expense.date = date_str
        self.expense_repo.update(expense)
        return expense

    def delete_expense(self, expense_id):
        expense = self.expense_repo.get_by_id(expense_id)
        if not expense:
            raise ValueError("Expense not found.")
        self.expense_repo.delete(expense_id)

    def total_spent(self):
        expenses = self.expense_repo.get_all()
        return sum(e.amount for e in expenses)

    def total_by_category(self):
        totals = {}
        expenses = self.expense_repo.get_all()
        for e in expenses:
            cat = self.category_repo.get_by_id(e.category_id)
            cat_name = cat.name if cat else "Unknown"
            totals[cat_name] = totals.get(cat_name, 0) + e.amount
        return totals