import time
import sqlite3
import functools

query_cache = {}
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('test.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query')
        if query in query_cache:
            print(" Returning cached result")
            return query_cache[query]
        print(" Executing query and caching result")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
if __name__ == '__main__':
    # First call will execute and cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First call result:", users)

    # Second call will use the cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second call result:", users_again)
