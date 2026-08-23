class DatabaseInitializer:
    def __init__(self, db):
        self.db = db

    def initialize(self):
        """Create tables only if they don't already exist."""
        required_tables = ["quizzes", "questions", "results"]
        all_exist = all(self.db.table_exists(t) for t in required_tables)

        if all_exist:
            return   # no action needed

        # Create tables in dependency order
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_index INTEGER NOT NULL,
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                taken_at TEXT NOT NULL,
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
            )
        """)
        self.db.commit()
        print("Database initialized.")