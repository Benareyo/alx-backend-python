import sqlite3

def print_all_users():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    print(users)

if __name__ == '__main__':
    print_all_users()
