class Budget:
    def __init__(self, budget_id=None, category_id=None, month="", amount=0.0):
        self.id = budget_id
        self.category_id = category_id
        self.month = month  # "YYYY-MM"
        self.amount = amount

    def __repr__(self):
        return f"Budget(id={self.id}, category_id={self.category_id}, month='{self.month}', amount={self.amount})"