import sqlite3 
import functools

"""your code goes here"""
def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = args[0]  # Assuming the first argument is the connection
        try:
            result = func(*args, **kwargs)
            conn.commit()  # Commit the transaction
            return result
        except Exception as e:
            conn.rollback()  # Rollback on error
            print(f"Transaction failed: {e}")
            raise
    return wrapper

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')