import os
import sys
import pandas as pd
import urllib.error
# - - - - - - - - - - - - - - -
from Code import SQL_Functions as sql_func


def extract_attacks_data(data_location, my_cursor, file_data='Attacks(Date)', debug=False):
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

                attacks_data = pd.read_csv(os.path.abspath('Data') + '/Debug_Data - Groups Only.csv',
                                           encoding='unicode_escape')

            elif file_data == 'Attacks':
                # Example to reading attacks database without dates #
                print("\n\033[43m {}\033[00m".format('WARNING'),
                      'You are using', "\033[33m {}\033[00m".format('DEBUG DATA !'))

                attacks_data = pd.read_csv(os.path.abspath('Data') + '/Debug_Data - Attacks.csv')

            else:   # default: 'Attacks(Date)':
                # Example to reading attacks database with dates #
                print("\n\033[43m {}\033[00m".format('WARNING'),
                      'You are using', "\033[33m {}\033[00m".format('DEBUG DATA !'))

                attacks_data = pd.read_csv(os.path.abspath('Data') + '/Debug_Data - Attacks+Dates.csv')

        else:
            if data_location == 'Drive':
                # Read server database, which can be in one of the forms of the options above #
                data_url = 'https://drive.google.com/file/d/1ST2htkVfrnOSHiLD_gMOJyHC3upEOsQn/view?usp=sharing'
                data_file = 'https://drive.google.com/uc?id=' + data_url.split('/')[-2]
                attacks_data = pd.read_csv(data_file, encoding='unicode_escape')

            elif data_location == 'SQL':
                attacks_data, _ = sql_func.show_table_data(my_cursor, 'attacks')

            else:   # default: 'Local'
                attacks_data = pd.read_csv(os.path.abspath('Data') + '/Attacks+Dates.csv',
                                           encoding='unicode_escape')

        return attacks_data


    # Show an Error in case of missing local debug file or the cloud data file and terminate the program #
    except (FileNotFoundError, urllib.error.HTTPError):
        print("\n\033[41m {}\033[00m".format('ERROR'),
              "\033[91m {}\033[00m".format('\'' + file_data + '\' DATA file cannot be found !'))
        sys.exit(1)


def extract_connections_data(data_location, my_cursor, debug=False):
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

        elif data_location == 'Drive':
            connections_url = 'https://drive.google.com/file/d/1Wm5h4HcCtuw3e9-mT6t-kEgEvGs2g4PL/view?usp=sharing'
            connections_file = 'https://drive.google.com/uc?id=' + connections_url.split('/')[-2]
            connections = pd.read_csv(connections_file)

        elif data_location == 'SQL':
            connections, _ = sql_func.show_table_data(my_cursor, 'groups_connections')

        else:   # default: 'Local'
            connections = pd.read_csv(os.path.abspath('Data') + '/Groups Connections.csv',
                                      encoding='unicode_escape')

    except (FileNotFoundError, urllib.error.HTTPError):
        print("\n\033[41m {}\033[00m".format('ERROR'),
              "\033[91m {}\033[00m".format('CONNECTIONS file cannot be found at the \''
                                           + data_location + '\' location !'
                                                             '\nThe program will proceed without this information'))
        connections = pd.DataFrame()

    return connections
