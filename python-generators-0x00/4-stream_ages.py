#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator that yields ages one by one from user_data"""
    conn = seed.connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    row = cursor.fetchone()
    while row:
        yield int(row[0])
        row = cursor.fetchone()

    cursor.close()
    conn.close()


def calculate_average_age():
    """Uses the generator to calculate average age"""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
