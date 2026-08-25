import os

class DatabaseInitializer:
    def __init__(self, db, covers_dir="book_covers"):
        self.db = db
        self.covers_dir = covers_dir

    def initialize(self):
        # Create covers directory if it doesn't exist
        if not os.path.exists(self.covers_dir):
            os.makedirs(self.covers_dir)

        required_tables = ["books", "members", "loans"]
        all_exist = all(self.db.table_exists(t) for t in required_tables)
        if all_exist:
            return

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                cover_path TEXT,
                available INTEGER NOT NULL DEFAULT 1
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                returned INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (member_id) REFERENCES members(id)
            )
        """)
        self.db.commit()
        print("Database initialized.")