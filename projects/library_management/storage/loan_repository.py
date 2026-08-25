from models.loan import Loan

class LoanRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, loan):
        self.db.execute(
            "INSERT INTO loans (book_id, member_id, loan_date, due_date, returned) VALUES (?, ?, ?, ?, ?)",
            (loan.book_id, loan.member_id, loan.loan_date, loan.due_date, 0)
        )
        self.db.commit()
        loan.id = self.db.last_row_id()
        return loan

    def get_active_loans_for_book(self, book_id):
        self.db.execute(
            "SELECT * FROM loans WHERE book_id = ? AND returned = 0",
            (book_id,)
        )
        row = self.db.fetchone()
        if row:
            return self._row_to_loan(row)
        return None

    def get_loans_for_member(self, member_id):
        self.db.execute(
            "SELECT * FROM loans WHERE member_id = ? ORDER BY loan_date DESC",
            (member_id,)
        )
        rows = self.db.fetchall()
        return [self._row_to_loan(row) for row in rows]

    def mark_returned(self, loan_id):
        self.db.execute(
            "UPDATE loans SET returned = 1 WHERE id = ?",
            (loan_id,)
        )
        self.db.commit()

    def get_overdue_loans(self, current_date):
        self.db.execute(
            "SELECT * FROM loans WHERE returned = 0 AND due_date < ?",
            (current_date,)
        )
        rows = self.db.fetchall()
        return [self._row_to_loan(row) for row in rows]

    def _row_to_loan(self, row):
        return Loan(
            loan_id=row["id"],
            book_id=row["book_id"],
            member_id=row["member_id"],
            loan_date=row["loan_date"],
            due_date=row["due_date"],
            returned=bool(row["returned"])
        )