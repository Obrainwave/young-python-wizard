class Account:
    def __init__(self, account_id=None, name="", account_type="checking",
                 initial_balance=0.0, currency="USD", created_at=""):
        self.id = account_id
        self.name = name
        self.account_type = account_type
        self.initial_balance = initial_balance
        self.currency = currency
        self.created_at = created_at

    def __repr__(self):
        return f"Account(id={self.id}, name='{self.name}', type='{self.account_type}')"