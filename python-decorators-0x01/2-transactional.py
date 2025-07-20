import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('test.db')  # Replace 'test.db' with your actual database file
        try:
            result = func(conn, *args, **kwargs)  # Pass connection as first argument
        finally:
            conn.close()
        return result
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if no error
            return result
        except Exception as e:
            conn.rollback()  # Rollback if error occurs
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

@with_db_connection
def initialize_database(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, name, email)
        VALUES (1, 'John Doe', 'old_email@example.com')
    ''')
    conn.commit()

if __name__ == '__main__':
    initialize_database() 
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
