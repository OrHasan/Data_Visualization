from dash import html
# - - - - - - - - - - - - - - -
from Code import functions as func


def init(attacks_data):
    global map_current_data
    map_current_data = attacks_data


def change_map_style(map_style, fig, store_data, screensize, color_axis, data_by_attacks):
    global map_current_data

    match map_style:
        case '3D':
            store_data['map_current_style'] = 'orthographic'

        case other:
            store_data['map_current_style'] = 'kavrayskiy7'

    if store_data['map_animation']:
        slider = fig['layout']['sliders'][0]

    fig, _, _ = func.create_map(map_current_data, store_data['map_current_style'], screensize, color_axis,
                                store_data['map_animation'], data_by_attacks)

    if store_data['map_animation']:
        func.change_frame(fig, slider)

    return fig, store_data


# Choice between Timeline & Summary map visuality #
def change_map_data(map_data, fig, store_data, attacks_data, attacks_sum, screensize, color_axis, data_by_attacks):
    global map_current_data

    match map_data:
        case 'Summarized':
            map_current_data = attacks_sum
            store_data['map_animation'] = False

        case other:
            map_current_data = attacks_data
            store_data['map_animation'] = True

    fig, _, _ = func.create_map(map_current_data, store_data['map_current_style'], screensize, color_axis,
                                store_data['map_animation'], data_by_attacks)

    if store_data['map_animation']:
        func.change_frame(fig, '', attacks_data["Date "].index[len(set(attacks_data["Date "])) - 1],
                          list(set(attacks_data["Date "]))[-1])

    return fig, store_data


def change_figure(data_view, fig, map_dropdown_style):
    # global map_current_data

    match data_view:
        case 'Bars View':
            map_style_dropdown = {'display': 'none'}
            map_data_dropdown = {'display': 'none'}
            map_display = {'display': 'none'}
            bars_display = {'display': 'block'}

        case other:
            map_style_dropdown = map_dropdown_style
            map_data_dropdown = map_dropdown_style
            map_display = {'display': 'block'}
            bars_display = {'display': 'none'}

    return map_style_dropdown, map_data_dropdown, map_display, bars_display, fig


def init_connections(n_intervals, fig, store_data, screensize, color_axis, data_by_attacks):
    global map_current_data
    print("updated")
    fig, _, _ = func.create_map(map_current_data, store_data['map_current_style'], screensize, color_axis,
                                store_data['map_animation'], data_by_attacks)
    return ""


# Click event - country selection #
def update_figure(click_data, fig, store_data, connections, screensize, color_axis, data_by_attacks, is_open):
    modal_title = ""
    modal_body = ""

    if click_data is not None:
        if store_data['map_animation']:
            slider = fig['layout']['sliders'][0]

        fig, groups_index, _ = func.create_map(map_current_data, store_data['map_current_style'], screensize,
                                               color_axis, store_data['map_animation'], data_by_attacks)

        location = click_data['points'][0]['location']
        location_groups = click_data['points'][0]['customdata'][groups_index]
        if not connections.empty:
            _, selections_connections, connections_countries, connections_countries_without_self =\
                func.check_connections(location, location_groups.split(", "), map_current_data, connections)

        print("In the country: ", location)
        print("There are the following attack groups: ", location_groups)

        if not connections.empty:
            print("Those groups are connected to the following groups: ", ', '.join(selections_connections))
            print("The connected groups are from the following countries: ", ', '.join(connections_countries))
            if connections_countries != connections_countries_without_self:
                print("The connected groups are from the following countries (without selected): ",
                      ', '.join(connections_countries_without_self))

            if connections_countries_without_self[0] != '(none)':
                for connect_location in connections_countries_without_self:
                    if connect_location != '(no info)':
                        func.show_connections(fig, [location, connect_location])
                        print([location, connect_location])

        if store_data['map_animation']:
            func.change_frame(fig, slider)
        is_open = not is_open

        modal_title = location + " Attack Groups"
        modal_body = html.Table([html.Tr(html.Td(item)) for item in map_current_data['Groups '][
                                 map_current_data[map_current_data['Country'] == location]
                                .index.tolist()[0]].split(', ')])

    return fig, is_open, modal_title, modal_body


def update_tab(n_clicks, store_data):
    if store_data['Tab'] == 'Show_Map':
        store_data['Tab'] = 'Update_DB'
        button_text = 'Return to Map View'
        map_display = {'display': 'none'}
        update_display = {'display': 'flex'}

    else:
        store_data['Tab'] = 'Show_Map'
        button_text = 'Change Database'
        map_display = {'display': 'block'}
        update_display = {'display': 'none'}

    return store_data, button_text, map_display, update_display


def toggle_dropdown(selected_option, store_data):
    match selected_option:
        case 'Show Data':
            store_data['Show_Data_Visible'] = True
            store_data['New_Country_Visible'] = False
            store_data['New_Groups_Visible'] = False
            show_data_display = {'display': 'block'}
            new_country_display = {'display': 'none'}
            new_groups_display = {'display': 'none'}

        case 'Add Country':
            store_data['Show_Data_Visible'] = False
            store_data['New_Country_Visible'] = True
            store_data['New_Groups_Visible'] = False
            show_data_display = {'display': 'none'}
            new_country_display = {'display': 'block'}
            new_groups_display = {'display': 'none'}

        case 'Add Groups':
            store_data['Show_Data_Visible'] = False
            store_data['New_Country_Visible'] = False
            store_data['New_Groups_Visible'] = True
            show_data_display = {'display': 'none'}
            new_country_display = {'display': 'none'}
            new_groups_display = {'display': 'block'}

    return show_data_display, new_country_display, new_groups_display, store_data


def update_groups(selected_country):
    groups_options = map_current_data['Groups '][1].split(', ')
    groups_value = map_current_data['Groups '][1].split(', ')[0]

    return groups_options, groups_value
