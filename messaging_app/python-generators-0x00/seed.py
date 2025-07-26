import csv
import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # Put your MySQL root password here if you have one
        )
        return conn
    except mysql.connector.Error as err:
        print("Cannot connect to MySQL:", err)
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        return conn
    except mysql.connector.Error as err:
        print("Cannot connect to ALX_prodev:", err)
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    """)
    cursor.close()

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()
def stream_rows(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    row = cursor.fetchone()  # get the first row
    while row:
        yield row          # "yield" returns one row at a time
        row = cursor.fetchone()  # get next row
    cursor.close()
