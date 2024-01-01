import os
import sys
sys.path.insert(1, os.path.abspath('Code'))
sys.path.insert(1, os.path.abspath('Code/Server'))
sys.path.insert(1, os.path.abspath('Code/Server/HTML Divisions'))

import ctypes
import pandas as pd
# - - - - - - - - - - - - - - -
from Code import Functions as Func
from Code.Server import Server


# Debug Section #
# Please DO NOT leave this section on debug mode while pushing the code!!

# Choice between:
# 'Server Data'(default), 'Groups-Debug', 'Attacks-Debug', 'Attacks(Date)-Debug'
file_data = 'Groups-Debug'


# Get the user screen size to set the map size #
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 150

if file_data == 'Groups-Debug':
    # Example to reading only groups database by country #
    print('\nYou are using', "\033[91m {}\033[00m".format('DEBUG DATA !'))

    attacks_data = pd.read_csv('D:/Or Hasan/Continuously BU - Personal/Fojects/Python/Projects'
                               '/DataVisualization/Data/Debug_Data - Groups Only.csv', encoding='unicode_escape')

elif file_data == 'Attacks-Debug':
    # Example to reading attacks database without dates #
    print('\nYou are using', "\033[91m {}\033[00m".format('DEBUG DATA !'))

    attacks_data = pd.read_csv('D:/Or Hasan/Continuously BU - Personal/Fojects/Python/Projects'
                               '/DataVisualization/Data/Debug_Data - Attacks.csv')

elif file_data == 'Attacks(Date)-Debug':
    # Example to reading attacks database with dates #
    print('\nYou are using', "\033[91m {}\033[00m".format('DEBUG DATA !'))

    attacks_data = pd.read_csv('D:/Or Hasan/Continuously BU - Personal/Fojects/Python/Projects'
                               '/DataVisualization/Data/Debug_Data - Attacks+Dates.csv')

else:
    # Read server database, which can be in one of the forms of the options above #
    import sys
    print("\n\033[91m {}\033[00m".format('MISSING CODE PART !'))
    sys.exit()


# Read groups connection map #
# connections = pd.DataFrame()
connections = pd.read_csv('D:\Or Hasan\Continuously BU - Personal\Fojects\Python\Projects'
                          '\DataVisualization\Data\Debug_Data - Groups Connections.csv')

# Check the type of the imported file #
# data_by_attacks = True - Database of the groups without the attacks amount
# data_by_attacks = False - Database with amount of attacks
data_by_attacks = "Attacks" in attacks_data.columns

# date_animation = True & data_by_attacks = True - Database with amount of attacks + Dates
date_animation = "Date" in attacks_data.columns


# # create a list of all the attack groups without duplicates from different dates #
# attack_groups = []
# for country_groups in attacks_data["Attack Groups"]:
#     if str(country_groups) != 'nan':
#         attack_groups = list(set(attack_groups + country_groups.split(", ")))
# # print(attack_groups)
#
# check_connections_test = ["Brown Chickens", "Anti Israel", "NotIran", "WeAreWithSomeVeryLongNameThatLooksTough"]
# print(check_connections(check_connections_test))


# # Get the country codes #
# country_codes = pd.read_csv('D:\Or Hasan\Continuously BU - Personal\Fojects\Python\Projects'
#                             '\DataVisualization\Data\Country Codes.csv', sep=",")
# x = 0
# country_code = [0 for i in range(len(attacks_data.index))]
#
# for Country in attacks_data["Country"]:
#     country_code[x] = country_codes[country_codes["Country"] == Country]["Alpha 3 Code"].item()
#     x = x+1

# print("Choice which data you want to see:\n"
#       "1. Amount of attacks by country\n"
#       "2. attack Frequency by country")
#
# # data_type = input()

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
fig, _, bars_fig = Func.create_map(attacks_data, map_style, screensize, color_axis, date_animation, data_by_attacks)

if date_animation:
    Func.change_frame(fig, '', attacks_data["Date "].index[len(set(attacks_data["Date "]))-1],
                      list(set(attacks_data["Date "]))[-1])

# Set the server and define events listeners #
app = Server.set_server(attacks_data, fig, bars_fig, connections, date_animation)
Server.events(app, attacks_data, attacks_sum, screensize, color_axis, connections, data_by_attacks)

app.run(debug=True)
# app.run_server(mode='inline')   #, debug=True)
