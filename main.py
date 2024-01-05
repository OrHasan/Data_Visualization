import os
import sys
import ctypes
import pandas as pd
import urllib.error
# - - - - - - - - - - - - - - -
sys.path.insert(1, os.path.abspath('Code'))
sys.path.insert(1, os.path.abspath('Code/Server'))
sys.path.insert(1, os.path.abspath('Code/Server/HTML Divisions'))
from Code import functions as func
from Code.Server import server


# Debug Section #
# Please DO NOT leave this section on debug mode while pushing the code!!

# Choice between:
# 'Server Data' (default), 'Groups-Debug', 'Attacks-Debug', 'Attacks(Date)-Debug'
file_data = 'Server Data'
# 'Server Data' (default), 'Debug Data'
connections_data = 'Server Data'


# Get the user screen size to set the map size #
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0) - 100, user32.GetSystemMetrics(1) - 150

try:
    if file_data == 'Groups-Debug':
        # Example to reading only groups database by country #
        print("\n\033[43m {}\033[00m".format('WARNING'), 'You are using', "\033[33m {}\033[00m".format('DEBUG DATA !'))

        attacks_data = pd.read_csv(os.path.abspath('Data') + '\Debug_Data - Groups Only.csv', encoding='unicode_escape')

    elif file_data == 'Attacks-Debug':
        # Example to reading attacks database without dates #
        print("\n\033[43m {}\033[00m".format('WARNING'), 'You are using', "\033[33m {}\033[00m".format('DEBUG DATA !'))

        attacks_data = pd.read_csv(os.path.abspath('Data') + '\Debug_Data - Attacks.csv')

    elif file_data == 'Attacks(Date)-Debug':
        # Example to reading attacks database with dates #
        print("\n\033[43m {}\033[00m".format('WARNING'), 'You are using', "\033[33m {}\033[00m".format('DEBUG DATA !'))

        attacks_data = pd.read_csv(os.path.abspath('Data') + '\Debug_Data - Attacks+Dates.csv')

    else:
        # Read server database, which can be in one of the forms of the options above #
            data_url = 'https://drive.google.com/file/d/1v_72gej13Zt1qur-COx38Dtdagl8ELnw/view?usp=sharing'
            data_file = 'https://drive.google.com/uc?id=' + data_url.split('/')[-2]
            attacks_data = pd.read_csv(data_file, encoding='unicode_escape')
            # attacks_data = pd.read_csv('https://drive.proton.me/urls/S6PMA6JKGR#ISZLhZRIx1We', encoding='unicode_escape')

# Show an Error in case of missing local debug file or the cloud data file and terminate the program #
except (FileNotFoundError, urllib.error.HTTPError):
    print("\n\033[41m {}\033[00m".format('ERROR'), "\033[91m {}\033[00m".format('\'' + file_data + '\' DATA file cannot be found !'))
    sys.exit(1)

# Read groups connection map #
try:
    if connections_data == 'Debug Data':
        print("\n\033[43m {}\033[00m".format('WARNING'), 'You are using', "\033[33m {}\033[00m".format('DEBUG CONNECTIONS DATA !'))
        connections_file = os.path.abspath('Data') + '\Debug_Data - Groups Connections.csv'
        connections = pd.read_csv(connections_file)
    else:
        # The Connections file is still not exist #
        connections_url = 'https://drive.google.com/file/d/????????????????????????????????????????????/view?usp=sharing'
        connections_file = 'https://drive.google.com/uc?id=' + connections_url.split('/')[-2]
        connections = pd.read_csv(connections_file)

except (FileNotFoundError, urllib.error.HTTPError):
    print("\n\033[41m {}\033[00m".format('ERROR'), "\033[91m {}\033[00m".format('\'' + connections_data + '\' CONNECTIONS file cannot be found !'))
    connections = pd.DataFrame()

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
# country_codes = pd.read_csv(os.path.abspath('Data') + '\Country Codes.csv', sep=",")
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
fig, _, bars_fig = func.create_map(attacks_data, map_style, screensize, color_axis, date_animation, data_by_attacks)

if date_animation:
    func.change_frame(fig, '', attacks_data["Date "].index[len(set(attacks_data["Date "])) - 1],
                      list(set(attacks_data["Date "]))[-1])

# Set the server and define events listeners #
app = server.set_server(attacks_data, fig, bars_fig, connections, date_animation)
server.events(app, attacks_data, attacks_sum, screensize, color_axis, connections, data_by_attacks)

app.run(debug=True)
# app.run_server(mode='inline')   #, debug=True)
