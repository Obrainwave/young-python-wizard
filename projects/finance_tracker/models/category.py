class Category:
    def __init__(self, category_id=None, name="", type="expense", color="#6c757d"):
        self.id = category_id
        self.name = name
        self.type = type  # "income" or "expense"
        self.color = color

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}', type='{self.type}')"