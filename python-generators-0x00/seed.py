import csv
import uuid
import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv


load_dotenv()

# Database credentials
HOST = os.environ.get('DB_HOST')
USER = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')
DATABASE = os.environ.get('DB_NAME')

def connect_db():
    # Connect to MySQL server
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: Check your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print("Error:", err)
    return connection

def create_database(connection):
    try:
        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: Check your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print("Error:", err)

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )

        # Select the database
        connection.database = DATABASE
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: Check your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print("Error:", err)
    return connection

def create_table(connection):
    try:
        cursor = connection.cursor()
        
        # Create table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX(user_id)
        );
        """
        cursor.execute(create_table_query)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: Check your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print("Error:", err)

def insert_data(connection, data):
    try:
        cursor = connection.cursor()

        with open(data, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(insert_query, (user_id, name, email, age))

        connection.commit()

    except FileNotFoundError:
        print(f"File {data} not found.")
    except KeyError as e:
        print(f"Missing expected column in CSV: {e}")
    except Exception as err:
        print(f"Error inserting data: {err}")
    finally:
        if cursor:
            cursor.close()

