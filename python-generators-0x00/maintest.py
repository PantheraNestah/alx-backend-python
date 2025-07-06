seed = __import__('seed')

connection = seed.connect_db()
if connection:
    print("Connection Successful!")
    connection.close()
else:
    print("Connection Failed!")