#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")

    while True:
        age = cursor.fetchone()
        if age is None:
            break
        yield age

    cursor.close()
    connection.close()

def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age[0]
        count += 1

    if count == 0:
        return 0

    return float(total_age / count)

if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")