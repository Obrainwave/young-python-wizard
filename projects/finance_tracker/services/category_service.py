from models.category import Category
from storage.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, db_path):
        self.repo = CategoryRepository(db_path)

    def create_category(self, name, type_, color="#6c757d"):
        if not name.strip():
            raise ValueError("Category name cannot be empty.")
        if type_ not in ("income", "expense"):
            raise ValueError("Category type must be 'income' or 'expense'.")
        category = Category(name=name.strip(), type=type_, color=color)
        return self.repo.insert(category)

    def get_category(self, category_id):
        return self.repo.get_by_id(category_id)

    def get_all_categories(self):
        return self.repo.get_all()

    def get_income_categories(self):
        return self.repo.get_by_type("income")

    def get_expense_categories(self):
        return self.repo.get_by_type("expense")

    def update_category(self, category_id, name, type_, color="#6c757d"):
        category = self.repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found.")
        if not name.strip():
            raise ValueError("Category name cannot be empty.")
        if type_ not in ("income", "expense"):
            raise ValueError("Category type must be 'income' or 'expense'.")
        category.name = name.strip()
        category.type = type_
        category.color = color
        self.repo.update(category)
        return category

    def delete_category(self, category_id):
        if not self.repo.get_by_id(category_id):
            return False
        self.repo.delete(category_id)
        return True