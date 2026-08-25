from models.book import Book

class BookRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, book):
        self.db.execute(
            "INSERT INTO books (title, author, isbn, cover_path, available) VALUES (?, ?, ?, ?, ?)",
            (book.title, book.author, book.isbn, book.cover_path, 1 if book.available else 0)
        )
        self.db.commit()
        book.id = self.db.last_row_id()
        return book

    def get_by_id(self, book_id):
        self.db.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = self.db.fetchone()
        if row:
            return self._row_to_book(row)
        return None

    def get_all(self):
        self.db.execute("SELECT * FROM books ORDER BY title")
        rows = self.db.fetchall()
        return [self._row_to_book(row) for row in rows]

    def search(self, term):
        self.db.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? ORDER BY title",
            (f"%{term}%", f"%{term}%", f"%{term}%")
        )
        rows = self.db.fetchall()
        return [self._row_to_book(row) for row in rows]

    def update(self, book):
        self.db.execute(
            "UPDATE books SET title = ?, author = ?, isbn = ?, cover_path = ?, available = ? WHERE id = ?",
            (book.title, book.author, book.isbn, book.cover_path, 1 if book.available else 0, book.id)
        )
        self.db.commit()

    def delete(self, book_id):
        self.db.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.db.commit()

    def _row_to_book(self, row):
        return Book(
            book_id=row["id"],
            title=row["title"],
            author=row["author"],
            isbn=row["isbn"],
            cover_path=row["cover_path"],
            available=bool(row["available"])
        )