import sqlite3
import csv
import uuid
from pathlib import Path

def setup_sqlite_db(db_name="users.db", csv_file="users.csv"):
    # Create/connect to the SQLite database in current directory
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        );
    ''')

    # Read from CSV and insert into users table
    csv_path = Path(csv_file)
    if not csv_path.exists():
        print(f"CSV file {csv_file} not found.")
        return

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name']
            email = row['email']
            age = int(row['age'])

            cursor.execute('''
                INSERT INTO users (name, email, age)
                VALUES (?, ?, ?)
            ''', (name, email, age))

    conn.commit()
    conn.close()
    print(f"Database {db_name} created and populated successfully.")

# Run it
if __name__ == "__main__":
    setup_sqlite_db()
