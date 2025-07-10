import sqlite3

class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open connection and cursor
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self.cursor  # So you can use this directly in the with block

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit if no exceptions, rollback if any
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.cursor.close()
            self.conn.close()

if __name__ == "__main__":
    db_file = "users.db"

    with DatabaseConnection(db_file) as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        for row in rows:
            print(row)
