class DatabaseInitializer:
    def __init__(self, db):
        self.db = db

    def initialize(self):
        required_tables = ["projects", "technologies", "project_technologies"]
        all_exist = all(self.db.table_exists(t) for t in required_tables)
        if all_exist:
            return

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                github_url TEXT,
                demo_url TEXT,
                date_created TEXT,
                featured INTEGER DEFAULT 0
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS technologies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS project_technologies (
                project_id INTEGER NOT NULL,
                technology_id INTEGER NOT NULL,
                PRIMARY KEY (project_id, technology_id),
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE
            )
        """)
        self.db.commit()
        print("Database initialized.")