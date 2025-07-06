seed = __import__('seed')

def stream_users_in_batches(batch_size):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            user_id, name, email, age = user
            if int(age) > 25:
                print(user)
                yield user
                #return