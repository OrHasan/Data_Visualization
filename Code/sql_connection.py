import mysql.connector
from mysql.connector import Error
import sys


def connect(password, host_name="localhost", user_name="root"):
    db_name = "cyber_attacks"

    try:
        db = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=password,
            database=db_name
        )
        if db.is_connected():
            print(f"Connected successfully to MySQL '{db_name}' database")
        return db, db.cursor()

    except Error as e:
        print(f"Error: {e}")
        print("\n\033[41m {}\033[00m".format('ERROR'),
              "\033[91m {}\033[00m".format('Failed to connect to MySQL \'' + db_name + '\' database !'))
        sys.exit(1)


def close(db, cursor):
    db.close()
    cursor.close()
