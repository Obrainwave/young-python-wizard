class DatabaseInitializer:
    def __init__(self, db):
        self.db = db

    def initialize(self):
        """Create tables only if they don't already exist."""
        required_tables = ["students", "courses", "assignments", "scores"]
        all_exist = all(self.db.table_exists(t) for t in required_tables)

        if all_exist:
            return   # nothing to do

        # Create tables in dependency order
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                max_score REAL NOT NULL,
                weight REAL NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                assignment_id INTEGER NOT NULL,
                score REAL NOT NULL,
                UNIQUE(student_id, assignment_id),
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (assignment_id) REFERENCES assignments(id)
            )
        """)
        self.db.commit()
        print("Database initialized.")