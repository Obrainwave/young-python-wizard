class DatabaseInitializer:
    def __init__(self, db):
        self.db = db

    def initialize(self):
        if self.db.table_exists("accounts"):
            return
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                account_type TEXT NOT NULL,
                initial_balance REAL DEFAULT 0,
                currency TEXT DEFAULT 'USD',
                created_at TEXT
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL,
                color TEXT DEFAULT '#6c757d'
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                category_id INTEGER,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                created_at TEXT,
                FOREIGN KEY (account_id) REFERENCES accounts(id),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                month TEXT NOT NULL,
                amount REAL NOT NULL,
                UNIQUE (category_id, month),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        self.db.commit()
        print("Database initialized.")