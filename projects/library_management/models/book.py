class Book:
    def __init__(self, book_id=None, title="", author="", isbn="", cover_path=None, available=True):
        self.id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.cover_path = cover_path
        self.available = available

    def __repr__(self):
        return (f"Book(id={self.id}, title='{self.title}', author='{self.author}', "
                f"isbn='{self.isbn}', cover_path='{self.cover_path}', available={self.available})")