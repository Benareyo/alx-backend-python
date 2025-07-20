import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')

# Clean existing rows and insert new test users
cursor.execute('DELETE FROM users')
cursor.execute('INSERT INTO users (name) VALUES ("Alice"), ("Bob")')

# Save changes and close
conn.commit()
conn.close()
