import os
import shutil
from datetime import date, timedelta
from models.book import Book
from models.member import Member
from models.loan import Loan
from storage.book_repository import BookRepository
from storage.member_repository import MemberRepository
from storage.loan_repository import LoanRepository

class LibraryService:
    def __init__(self, db, covers_dir="book_covers"):
        self.book_repo = BookRepository(db)
        self.member_repo = MemberRepository(db)
        self.loan_repo = LoanRepository(db)
        self.covers_dir = covers_dir

    # Book operations
    def add_book(self, title, author, isbn="", cover_source=None):
        if not title.strip() or not author.strip():
            raise ValueError("Title and author are required.")
        cover_path = None
        if cover_source:
            cover_path = self._save_cover(cover_source, title)
        book = Book(
            title=title.strip(),
            author=author.strip(),
            isbn=isbn.strip(),
            cover_path=cover_path,
            available=True
        )
        return self.book_repo.insert(book)

    def _save_cover(self, cover_source, title):
        """Save a cover image file to the covers directory. Returns the new path."""
        if not os.path.exists(self.covers_dir):
            os.makedirs(self.covers_dir)
        # Generate a safe filename from title
        safe_title = "".join(c if c.isalnum() else "_" for c in title).rstrip("_")
        ext = os.path.splitext(cover_source)[1] if os.path.isfile(cover_source) else ".jpg"
        dest = os.path.join(self.covers_dir, f"{safe_title}{ext}")
        if os.path.isfile(cover_source):
            shutil.copy(cover_source, dest)
        else:
            # If cover_source is not a file, we could download or handle differently
            # For now, just copy if it's a file; otherwise, leave as None
            return None
        return dest

    def update_book_cover(self, book_id, cover_source):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found.")
        # Delete old cover if exists
        if book.cover_path and os.path.isfile(book.cover_path):
            os.remove(book.cover_path)
        # Save new cover
        new_cover = self._save_cover(cover_source, book.title)
        book.cover_path = new_cover
        self.book_repo.update(book)

    def get_all_books(self):
        return self.book_repo.get_all()

    def search_books(self, term):
        return self.book_repo.search(term)

    def update_book(self, book_id, title, author, isbn):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found.")
        book.title = title.strip()
        book.author = author.strip()
        book.isbn = isbn.strip()
        self.book_repo.update(book)

    def delete_book(self, book_id):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found.")
        active_loan = self.loan_repo.get_active_loans_for_book(book_id)
        if active_loan:
            raise ValueError("Cannot delete a book that is currently borrowed.")
        # Delete cover file
        if book.cover_path and os.path.isfile(book.cover_path):
            os.remove(book.cover_path)
        self.book_repo.delete(book_id)

    # Member operations
    def add_member(self, name, email=""):
        if not name.strip():
            raise ValueError("Name is required.")
        member = Member(name=name.strip(), email=email.strip())
        return self.member_repo.insert(member)

    def get_all_members(self):
        return self.member_repo.get_all()

    def search_members(self, term):
        return self.member_repo.search(term)

    # Loan operations
    def borrow_book(self, book_id, member_id):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found.")
        if not book.available:
            raise ValueError("Book is already borrowed.")
        member = self.member_repo.get_by_id(member_id)
        if not member:
            raise ValueError("Member not found.")

        loan_date = date.today().isoformat()
        due_date = (date.today() + timedelta(days=14)).isoformat()
        loan = Loan(book_id=book_id, member_id=member_id, loan_date=loan_date, due_date=due_date)
        loan = self.loan_repo.insert(loan)

        book.available = False
        self.book_repo.update(book)

        return loan

    def return_book(self, book_id):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found.")
        if book.available:
            raise ValueError("Book is not currently borrowed.")

        active_loan = self.loan_repo.get_active_loans_for_book(book_id)
        if not active_loan:
            raise ValueError("No active loan found for this book.")

        self.loan_repo.mark_returned(active_loan.id)
        book.available = True
        self.book_repo.update(book)

    def get_member_loans(self, member_id):
        return self.loan_repo.get_loans_for_member(member_id)

    def get_overdue_loans(self):
        current_date = date.today().isoformat()
        return self.loan_repo.get_overdue_loans(current_date)