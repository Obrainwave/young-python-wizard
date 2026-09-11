class Transaction:
    def __init__(self, transaction_id=None, account_id=None, category_id=None,
                 type="expense", amount=0.0, description="", date="", created_at=""):
        self.id = transaction_id
        self.account_id = account_id
        self.category_id = category_id
        self.type = type
        self.amount = amount
        self.description = description
        self.date = date
        self.created_at = created_at

    def __repr__(self):
        return (f"Transaction(id={self.id}, type='{self.type}', "
                f"amount={self.amount}, date='{self.date}')")