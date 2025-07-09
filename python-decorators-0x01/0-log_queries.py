import sqlite3


def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('DELETE FROM users')  # Clear existing data
    cursor.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))
    cursor.execute('INSERT INTO users (name) VALUES (?)', ('Bob',))
    conn.commit()
    conn.close()

init_db()

import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Try to find the SQL query passed to the function
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] No SQL query found.")
        
        # Call the original function
        return func(*args, **kwargs)
    
    return wrapper

# Function that fetches users from the DB
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Run the function to test
users = fetch_all_users(query="SELECT * FROM users")
print(users)
