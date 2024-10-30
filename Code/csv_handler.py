import os
import sys
import pandas as pd
import urllib.error
# - - - - - - - - - - - - - - -
from Code import sql_connection as sql_con, SQL_Functions as sql_func


def extract_attacks_data(file_data, debug=False):
    my_cursor, db = '', ''
    if not debug:
        debug = {
            "attacks": False,
            "connections": False
        }

    try:
        if debug["attacks"]:
            if file_data == 'Groups':
                # Example to reading only groups database by country #
                print("\n\033[43m {}\033[00m".format('WARNING'),
                      'You are using', "\033[33m {}\033[00m".format('DEBUG DATA !'))

                attacks_data = pd.read_csv(os.path.abspath('Data') + '\Debug_Data - Groups Only.csv',
                                           encoding='unicode_escape')

            elif file_data == 'Attacks':
                # Example to reading attacks database without dates #
                print("\n\033[43m {}\033[00m".format('WARNING'),
                      'You are using', "\033[33m {}\033[00m".format('DEBUG DATA !'))

                attacks_data = pd.read_csv(os.path.abspath('Data') + '\Debug_Data - Attacks.csv')

            else:   # default: 'Attacks(Date)':
                # Example to reading attacks database with dates #
                print("\n\033[43m {}\033[00m".format('WARNING'),
                      'You are using', "\033[33m {}\033[00m".format('DEBUG DATA !'))

                attacks_data = pd.read_csv(os.path.abspath('Data') + '\Debug_Data - Attacks+Dates.csv')

        else:
            if file_data == 'Server Data':
                # Read server database, which can be in one of the forms of the options above #
                data_url = 'https://drive.google.com/file/d/1v_72gej13Zt1qur-COx38Dtdagl8ELnw/view?usp=sharing'
                data_file = 'https://drive.google.com/uc?id=' + data_url.split('/')[-2]
                attacks_data = pd.read_csv(data_file, encoding='unicode_escape')
                # attacks_data = pd.read_csv('https://drive.proton.me/urls/S6PMA6JKGR#ISZLhZRIx1We',
                #                            encoding='unicode_escape')

            else:   # default: 'SQL Data'
                host_name = input("Please enter the SQL Host Name (default: 'localhost'): ")
                host_name = 'localhost' if not host_name else host_name
                user_name = input("Please enter the SQL User Name (default: 'root'): ")
                user_name = 'root' if not user_name else user_name
                password = input("Please enter the SQL Password: ")

                db, my_cursor = sql_con.connect(password, host_name, user_name)
                attacks_data, _ = sql_func.show_table_data(my_cursor, 'attacks')

        return attacks_data, db, my_cursor


    # Show an Error in case of missing local debug file or the cloud data file and terminate the program #
    except (FileNotFoundError, urllib.error.HTTPError):
        print("\n\033[41m {}\033[00m".format('ERROR'),
              "\033[91m {}\033[00m".format('\'' + file_data + '\' DATA file cannot be found !'))
        sys.exit(1)


def extract_connections_data(file_data, my_cursor, debug=False):
    # Read groups connection map #
    if not debug:
        debug = {
            "attacks": False,
            "connections": False
        }

    try:
        if debug["connections"]:
            print("\n\033[43m {}\033[00m".format('WARNING'), 'You are using', "\033[33m {}\033[00m".format('DEBUG CONNECTIONS DATA !'))
            connections_file = os.path.abspath('Data') + '\Debug_Data - Groups Connections.csv'
            connections = pd.read_csv(connections_file)

        elif file_data == 'Server Data':
            # The Connections file is still not exist #
            connections_url = 'https://drive.google.com/file/d/????????????????????????????????????????????/view?usp=sharing'
            connections_file = 'https://drive.google.com/uc?id=' + connections_url.split('/')[-2]
            connections = pd.read_csv(connections_file)

        else:   # default: 'SQL Data'
            connections, _ = sql_func.show_table_data(my_cursor, 'groups_connections')

    except (FileNotFoundError, urllib.error.HTTPError):
        print("\n\033[41m {}\033[00m".format('ERROR'), "\033[91m {}\033[00m".format('\'' + connections_data + '\' CONNECTIONS file cannot be found !'))
        connections = pd.DataFrame()

    return connections
