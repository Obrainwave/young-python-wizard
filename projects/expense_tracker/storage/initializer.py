class DatabaseInitializer:
    def __init__(self, db):
        self.db = db

    def initialize(self):
        """Create tables only if they don't already exist."""
        required_tables = ["categories", "expenses"]
        all_exist = all(self.db.table_exists(t) for t in required_tables)

        if all_exist:
            return   # nothing to do

        # Create tables in dependency order
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        self.db.commit()
        print("Database initialized.")