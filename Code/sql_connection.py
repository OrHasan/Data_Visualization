import mysql.connector
from mysql.connector import Error
import sys


def connect():
    db_name = "cyber_attacks"
    for i in range(3):
        host_name = input("Please enter the SQL Host Name (default: 'localhost'): ")
        host_name = 'localhost' if not host_name else host_name
        user_name = input("Please enter the SQL User Name (default: 'root'): ")
        user_name = 'root' if not user_name else user_name
        password = input("Please enter the SQL Password: ")

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
            if i != 2:
                print("\n\033[43m {}\033[00m".format('WARNING') +
                      "\033[33m {}\033[00m".format(
                          'Failed to connect with the following input parameters:'
                          f'\n Host Name:       {host_name}'
                          f'\n User Name:       {user_name}'
                          f'\n Database Name:   {db_name}'
                          '\n\nPlease try again\n'))
            else:
                print(f"Error: {e}")
                print("\n\033[41m {}\033[00m".format('ERROR'),
                      "\033[91m {}\033[00m".format('Failed to connect to MySQL \'' + db_name + '\' database !'))
                sys.exit(1)


def close(db, cursor):
    db.close()
    cursor.close()
