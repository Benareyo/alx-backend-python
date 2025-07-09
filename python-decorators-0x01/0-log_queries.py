import sqlite3
import functools

# Setup the users table and sample data
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('DELETE FROM users')  # Clear table before inserting
    cursor.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))
    cursor.execute('INSERT INTO users (name) VALUES (?)', ('Bob',))
    conn.commit()
    conn.close()

init_db()

# Decorator that logs the SQL query
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

# Function to fetch all users
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Run the function and print result
users = fetch_all_users(query="SELECT * FROM users")
print(users)
