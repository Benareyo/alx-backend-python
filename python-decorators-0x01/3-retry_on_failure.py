import time
import sqlite3
import functools
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('test.db')  # Use the name of your database file
        try:
            result = func(conn, *args, **kwargs)  # Pass the connection to the function
        finally:
            conn.close()  # Always close the connection
        return result
    return wrapper
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        print("All retries failed.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
if __name__ == '__main__':
    users = fetch_users_with_retry()
    print(users)
