import sqlite3

class Database:
    def __init__(self, db_path="student_management.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Open a connection and create a cursor."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the connection if open."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def commit(self):
        """Commit the current transaction."""
        if self.conn:
            self.conn.commit()

    def execute(self, sql, params=()):
        """Execute a SQL statement using the cursor."""
        self.cursor.execute(sql, params)

    def fetchone(self):
        """Fetch one row from the cursor."""
        return self.cursor.fetchone()

    def fetchall(self):
        """Fetch all rows from the cursor."""
        return self.cursor.fetchall()

    def last_row_id(self):
        """Return the last inserted row id."""
        return self.cursor.lastrowid

    def table_exists(self, table_name):
        """Check if a table exists."""
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return self.cursor.fetchone() is not None