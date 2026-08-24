class Expense:
    def __init__(self, expense_id=None, category_id=None, amount=0.0, description="", date=""):
        self.id = expense_id
        self.category_id = category_id
        self.amount = amount
        self.description = description
        self.date = date   # format: YYYY-MM-DD

    def __repr__(self):
        return (f"Expense(id={self.id}, category_id={self.category_id}, "
                f"amount={self.amount}, description='{self.description}', date='{self.date}')")