import sqlite3
import functools

# Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open DB
        try:
            result = func(conn, *args, **kwargs)  # Call original function with DB
            return result
        finally:
            conn.close()  # Always close the DB
    return wrapper

# Function that fetches a user by ID, connection is passed automatically!
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Run the function
user = get_user_by_id(user_id=1)
print(user)
