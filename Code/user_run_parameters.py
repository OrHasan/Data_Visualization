import sys
# - - - - - - - - - - - - - - -
from Code import sql_connection as sql_con


def get_user_params():
    db_location = ''
    my_cursor, db = '', ''
    debug_file_data = ''
    # debug only works with csv combination (local pre-made file)
    debug_mode = input("Please choose if to use debug mode by the option number (1/2/3/4):"
                       "\n 1. Real Data"
                       "\n 2. Attacks Pre-made Data, With Real Groups Connections Data"
                       "\n 3. Groups Connections Pre-made Data, With Real Attacks Data"
                       "\n 4. Full Debug (local)\n")

    for i in range(5):
        match int(debug_mode):
            case 1:
                print("(Debug files in use: None)\n")
                debug = {
                    "attacks": False,
                    "connections": False
                }
                break
            case 2:
                print("(Debug file in use: Attacks Data)\n")
                debug = {
                    "attacks": True,
                    "connections": False
                }
                break
            case 3:
                print("(Debug file in use: Connections Data)\n")
                debug = {
                    "attacks": False,
                    "connections": True
                }
                break
            case 4:
                print("(Debug files in use: All)\n")
                db_location = "local"
                debug = {
                    "attacks": True,
                    "connections": True
                }
                break
            case _:
                if i != 4:
                    debug_mode = input("\n\033[43m {}\033[00m".format('WARNING') +
                                       "\033[33m {}\033[00m".format('You entered invalid debug option number,'
                                                                    ' please re-enter your selection (1, 2, 3 or 4)\n'))
                else:
                    print("\n\033[41m {}\033[00m".format('ERROR'),
                          "\033[91m {}\033[00m".format('You entered invalid value too many times,'
                                                       ' please re-run the program'))
                    sys.exit(1)

    if int(debug_mode) == 2 or int(debug_mode) == 4:
        debug_data = input("Please choose debug attacks file to load by the option number (1/2/3):"
                           "\n 1. Attacks + Dates"
                           "\n 2. Attacks Only"
                           "\n 3. Groups Only\n")

        for i in range(5):
            match int(debug_data):
                case 1:
                    print("(Debug file type: Attacks + Dates)\n")
                    debug_file_data = 'Attacks(Date)'
                    break
                case 2:
                    print("(Debug file type: Attacks Only)\n")
                    debug_file_data = 'Attacks'
                    break
                case 3:
                    print("(Debug file type: Groups Only)\n")
                    debug_file_data = 'Groups'
                    break
                case _:
                    if i != 4:
                        debug_data = input("\n\033[43m {}\033[00m".format('WARNING') +
                                           "\033[33m {}\033[00m".format('You entered invalid debug data option number,'
                                                                        ' please re-enter your selection (1, 2 or 3)\n'))
                    else:
                        print("\n\033[41m {}\033[00m".format('ERROR'),
                              "\033[91m {}\033[00m".format('You entered invalid value too many times,'
                                                           ' please re-run the program'))
                        sys.exit(1)

    if not db_location:
        data_location = input("Please choose the real data location by the option number (1/2/3):"
                              "\n 1. Drive (cloud)"
                              "\n 2. MySQL"
                              "\n 3. Local (./DataVisualization/Data/Attacks.csv &"
                              " ./DataVisualization/Data/Groups Connections.csv)\n")

        for i in range(5):
            match int(data_location):
                case 1:
                    print("(Data location: Drive)\n")
                    db_location = "Drive"
                    break
                case 2:
                    print("(Data location: MySQL)\n")
                    db_location = "SQL"
                    db, my_cursor = sql_con.connect()
                    break
                case 3:
                    print("(Data location: Local)\n")
                    db_location = "Local"
                    break
                case _:
                    if i != 4:
                        data_location = input("\n\033[43m {}\033[00m".format('WARNING') +
                                              "\033[33m {}\033[00m".format(
                                                  'You entered invalid data location option number,'
                                                  ' please re-enter your selection (1, 2 or 3)\n'))
                    else:
                        print("\n\033[41m {}\033[00m".format('ERROR'),
                              "\033[91m {}\033[00m".format('You entered invalid value too many times,'
                                                           ' please re-run the program'))
                        sys.exit(1)

    return db_location, db, my_cursor, debug, debug_file_data
