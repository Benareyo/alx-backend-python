import sqlite3

def setup_users_table():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # Create users table if it doesn't exist (without age column initially)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')

    # Check if 'age' column exists in users table
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'age' not in columns:
        # Add the age column if it doesn't exist
        cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")

    # Insert sample user if table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ('John Doe', 'Crawford_Cartwright@hotmail.com', 30)
        )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_users_table()
    print("Database initialized with users table and sample data.")
