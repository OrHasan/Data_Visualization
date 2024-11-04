import os
import sys
import ctypes
# - - - - - - - - - - - - - - -
sys.path.insert(1, os.path.abspath('Code'))
sys.path.insert(1, os.path.abspath('Code/Server'))
sys.path.insert(1, os.path.abspath('Code/Server/HTML Divisions'))
# Don't change the following import code order,
# as it important to load "mysql.connector" before the "dash" library (otherwise, error code "0xC0000005" will rise)
from Code import user_run_parameters as user_params, sql_connection as sql_con, csv_handler
from Code import functions as func
from Code.Server import server


def build_map():
    db_location, db, my_cursor, debug, debug_file_data = user_params.get_user_params()

    # Get the user screen size to set the map size #
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 150

    attacks_data = csv_handler.extract_attacks_data(db_location, my_cursor, debug_file_data, debug)
    connections = csv_handler.extract_connections_data(db_location, my_cursor, debug)


    # Check the type of the imported file #
    # data_by_attacks = True - Database of the groups without the attacks amount
    # data_by_attacks = False - Database with amount of attacks
    data_by_attacks = "Attacks" in attacks_data.columns

    # date_animation = True & data_by_attacks = True - Database with amount of attacks + Dates
    date_animation = "Date" in attacks_data.columns

    map_style = 'kavrayskiy7'
    # Rename the columns names inside the code (name with space are for visual reasons) #
    attacks_data = attacks_data.rename(
        columns={
            "Date": "Date ",
            "Attacks": "Attacks ",
            "Frequency": "Frequency ",
            "Attack Groups": "Groups ",
            # "Group": "Groups "
        }
    ).fillna("(no info)")

    # Sum the data from all the dates to a single frame #
    if data_by_attacks:
        if date_animation:
            attacks_sum = attacks_data.groupby('Country')['Attacks '].sum().reset_index()
            # Check the last known groups for each country #
            last_known_groups = lambda x: attacks_data.loc[(attacks_data['Country'] == x) &
                                                           (attacks_data['Date '] ==
                                                            attacks_data['Date '][attacks_data['Country'] == x]
                                                            .max()), 'Groups '].values[0]
            attacks_sum['Groups '] = attacks_sum['Country'].apply(last_known_groups)

        else:
            attacks_sum = ""

    # Create the data based on number of groups from each country #
    else:
        attacks_data = attacks_data.groupby('Country')['Group'].apply(list).reset_index(name='Groups ')
        attacks_data['Groups Amount '] = attacks_data['Groups '].apply(lambda x: len(x))
        attacks_data['Groups '] = attacks_data['Groups '].apply(lambda x: ', '.join(x))
        attacks_sum = ""

    color_axis = f"coloraxis{2}"
    fig, _, bars_fig = func.create_map(attacks_data, map_style, screensize, color_axis, date_animation, data_by_attacks)

    if date_animation:
        func.change_frame(fig, '', attacks_data["Date "].index[len(set(attacks_data["Date "])) - 1],
                          list(set(attacks_data["Date "]))[-1])

    # Set the server and define events listeners #
    app = server.set_server(attacks_data, fig, bars_fig, connections, date_animation, db_location)
    server.events(app, attacks_data, attacks_sum, screensize, color_axis, connections, data_by_attacks)

    return app, db_location, db, my_cursor


app = ''
if __name__ == '__main__':
    app, location, db, my_cursor = build_map()

    app.run(debug=False)
    # app.run_server(mode='inline')   #, debug=True)

    if location == 'SQL':
        sql_con.close(db, my_cursor)
