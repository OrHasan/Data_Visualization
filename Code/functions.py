import plotly.express as pl_exp
from dash import html
import numpy as np


def create_map(attacks_data, map_style, screensize, color_axis, date_animation, data_by_attacks):
    # Create a single data map #
    if data_by_attacks:
        color_data = 'Attacks '
        colors_type = 'YlOrRd'
        graph_title = 'Cyber Attacks on Israel'

    else:
        color_data = 'Groups Amount '
        colors_type = 'YlOrRd'
        graph_title = 'Cyber Attack Groups by Country'

    # Choice which data to show when hovering over a country with the mouse and the values types if needed #
    if data_by_attacks:
        if date_animation:
            hover_data = {
                "Date ": True,
                "Country": False,
                "Attacks ": ": ,d",
                # "Frequency ": ": ,d",
                "Groups ": False,
            }

        else:
            hover_data = {
                "Country": False,
                "Attacks ": ": ,d",
                # "Frequency ": ": ,d",
                "Groups ": False,
            }
    else:
        hover_data = {
            "Country": False,
            "Groups Amount ": ": ,d",
            "Groups ": False,
        }

    # Find the index of "Groups" inside hover_data
    groups_index = list(hover_data).index('Groups ')

    # if data_by_attacks:
    if date_animation and data_by_attacks:
        fig = pl_exp.choropleth(attacks_data, locations='Country', color=color_data, hover_name='Country',
                                hover_data=hover_data, projection=map_style, animation_frame='Date ',
                                title=graph_title, locationmode='country names', color_continuous_scale=colors_type,
                                height=screensize[1]-150)

        bars_fig = pl_exp.bar(attacks_data, x="Country", y=color_data, color=color_data,
                              hover_data=hover_data)

    else:
        fig = pl_exp.choropleth(attacks_data, locations='Country', color=color_data, hover_name='Country',
                                hover_data=hover_data, projection=map_style,
                                title=graph_title, locationmode='country names', color_continuous_scale=colors_type,
                                height=screensize[1]-150)

        bars_fig = pl_exp.bar(attacks_data, x="Country", y=color_data, color=color_data,
                              hover_data=hover_data)

    # Settings for the color map index like: settings his minimum & maximum values and adding a title above it #
    fig = fig.update_layout(
        {
            color_axis: {
                "cmin": attacks_data[color_data].replace(0, np.nan).quantile(0.1),
                "cmax": attacks_data[color_data].replace(0, np.nan).quantile(0.9),
                "colorbar": {"title": color_data},
            }
        }
    )

    # Update map settings #
    fig.update_layout(
        geo=dict(
            resolution=50,  # 50 - more details
            showland=True,
            showlakes=True,
            landcolor='rgb(204, 204, 204)',
            countrycolor='rgb(204, 204, 204)',
            lakecolor='rgb(255, 255, 255)',
        ),

        margin={"l": 0, "r": 0, "t": 75, "b": 0},
        clickmode="event+select",
    )

    return fig, groups_index, bars_fig


def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns])
            for i in range(len(dataframe))
        ])
    ])


def check_connections(country, groups, attacks_data, connections):
    if groups[0] != '(no info)':
        country_connections = []
        connected_countries = []

        for group in groups:
            country_groups_and_connections = list(set(country_connections + list(connections[group])))
            country_connections = list(set(country_groups_and_connections) - set(groups))

        country_groups_and_connections = [x for x in country_groups_and_connections if str(x) != 'nan']
        country_connections = [x for x in country_connections if str(x) != 'nan']

        if country_connections:
            for connected_group in country_connections:
                connected_countries = list(set(connected_countries + list(attacks_data['Country'][[idx for idx, text in
                                               enumerate(attacks_data['Groups ']) if connected_group in text]])))
        try:
            country_connections_without_self = list(connected_countries).remove(country)
        except ValueError:
            country_connections_without_self = connected_countries

        if not country_groups_and_connections:
            country_groups_and_connections = ['(none)']

        if not country_connections:
            country_connections = ['(none)']

        if not connected_countries:
            connected_countries = ['(none)']

        if not country_connections_without_self:
            country_connections_without_self = ['(none)']

        return country_groups_and_connections, country_connections,\
               connected_countries, country_connections_without_self

    else:
        return ['(no info)'], ['(no info)'], ['(no info)'], ['(no info)']


def show_connections(fig, countries):
    # Add lines connecting between countries #
    fig.add_scattergeo(
        locations=countries,
        locationmode="country names",
        # text=attacks_data['Attacks '],
        mode='lines+markers',
        hoverinfo='skip'
    )


def change_frame(fig, slider, frame_number=np.nan, frame_name=''):
    if np.isnan(frame_number) or frame_name == '':
        frame_number = slider['active']

    fig.layout.sliders[0].active = frame_number
    fig.data[0].update(fig.frames[frame_number].data[0])
