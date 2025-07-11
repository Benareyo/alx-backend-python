import sqlite3

def update_user_age():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # Update age for existing users with NULL age
    cursor.execute("UPDATE users SET age = 30 WHERE age IS NULL")

    conn.commit()
    conn.close()
    print("Updated user ages where age was NULL.")

if __name__ == '__main__':
    update_user_age()
