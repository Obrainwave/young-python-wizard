class Loan:
    def __init__(self, loan_id=None, book_id=None, member_id=None, loan_date="", due_date="", returned=False):
        self.id = loan_id
        self.book_id = book_id
        self.member_id = member_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.returned = returned

    def __repr__(self):
        return (f"Loan(id={self.id}, book_id={self.book_id}, member_id={self.member_id}, "
                f"loan_date='{self.loan_date}', due_date='{self.due_date}', returned={self.returned})")