class DatabaseInitializer:
    def __init__(self, db):
        self.db = db

    def initialize(self):
        if self.db.table_exists("documents"):
            return
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                embedding TEXT NOT NULL
            )
        """)
        self.db.commit()
        print("Database initialized.")