import sqlite3

class ExecuteQuery:
    def __init__(self, db_path, query, params=None):
        """
        Custom context manager for executing a SQL query safely.
        Args:
            db_path (str): Path to the SQLite database.
            query (str): SQL query string.
            params (tuple/list): Parameters for parameterized query.
        """
        self.db_path = db_path
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Execute the query
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()  # Get all rows
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

if __name__ == "__main__":
    db_file = "users.db"
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery(db_file, query, param) as results:
        for row in results:
            print(row)
