class DatabaseInitializer:
    def __init__(self, db):
        self.db = db

    def initialize(self):
        """Create tables only if they don't already exist."""
        if self.db.table_exists("password_history"):
            return   # table already exists

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS password_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT NOT NULL,
                length INTEGER NOT NULL,
                char_types TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.db.commit()
        print("Database initialized.")