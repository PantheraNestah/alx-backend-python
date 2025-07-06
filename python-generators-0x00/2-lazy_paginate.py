#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    A generator function that yields a page of user data from the database.
    The page size is determined by the `page_size` parameter.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        
        yield page
        offset += page_size

