class DatabaseInitializer:
    def __init__(self, db):
        self.db = db

    def initialize(self):
        if self.db.table_exists("projects"):
            return
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                image_url TEXT,
                github_url TEXT,
                live_url TEXT,
                date_created TEXT,
                featured INTEGER DEFAULT 0
            )
        """)
        self.db.commit()
        print("Database initialized.")