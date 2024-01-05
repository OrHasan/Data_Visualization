import plotly.express as pl_exp
# import plotly.graph_objects as pl_go
from dash import html
import numpy as np


def create_map(attacks_data, map_style, screensize, color_axis, date_animation, data_by_attacks):
    # # Create multi data maps kinds #
    # for data_type in range(2):
    #     match data_type:
    #         case 0:
    #             color_data = 'Attacks '
    #             colors_type = 'YlOrRd'
    #             graph_title = 'Cyber Attacks on Israel'
    #
    #         case other:
    #             fig = temp_fig
    #
    #             color_data = 'Frequency '
    #             colors_type = 'Blues'
    #             graph_title = 'Attack Frequency on Israel'
    #
    #     temp_fig = pl_exp.choropleth(attacks_data, locations='Country', color=color_data, hover_name='Country',
    #                                  hover_data=hover_data, projection=map_style, animation_frame='Date ',
    #                                  title=graph_title, locationmode='country names', color_continuous_scale=colors_type,
    #                                  height=screensize[1])    # .update_traces(visible=False, coloraxis=color_axis)
    #
    # fig.add_trace(temp_fig.data[0])
    # for i, frame in enumerate(fig.frames):
    #     fig.frames[i].data += (temp_fig.frames[i].data[0],)

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
                                height=screensize[1]-150)   #.update_traces(visible=False, coloraxis=color_axis)

        # bars_fig = pl_exp.bar(attacks_data, x="Country", y=color_data, color='Groups ', animation_frame='Date ',
        #                       hover_data=hover_data)
        bars_fig = pl_exp.bar(attacks_data, x="Country", y=color_data, color=color_data,
                              hover_data=hover_data)  # pattern_shape='Groups ' , pattern_shape_sequence=[".", "x", "+"])

    else:
        fig = pl_exp.choropleth(attacks_data, locations='Country', color=color_data, hover_name='Country',
                                hover_data=hover_data, projection=map_style,
                                title=graph_title, locationmode='country names', color_continuous_scale=colors_type,
                                height=screensize[1]-150)

        bars_fig = pl_exp.bar(attacks_data, x="Country", y=color_data, color=color_data,
                              hover_data=hover_data)

    # else:
    #     fig = pl_exp.choropleth(attacks_data, locations='Country', color=color_data, hover_name='Country',
    #                             hover_data=hover_data, projection=map_style,
    #                             title=graph_title, locationmode='country names', color_continuous_scale=colors_type,
    #                             height=screensize[1] - 100)  # .update_traces(visible=False, coloraxis=color_axis)

    # fig.update_layout(coloraxis_showscale=False)

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

    # # Add line by lat. & lon. #
    # fig2 = pl_go.Figure(data=pl_go.Scattergeo(
    #                     lat=[40.7127, 51.5072],
    #                     lon=[-74.0059, 0.1275],
    #                     mode='lines',
    #                     line=dict(width=2, color='blue'),
    #                     ))
    #
    # fig.add_trace(fig2.data[0])

    # Update map settings #
    # maps_titles = ["Total Attacks", "Attack Frequency"]
    fig.update_layout(
        # title_text='Test',
        # showlegend=True,
        geo=dict(
            resolution=50,  # 50 - more details
            showland=True,
            showlakes=True,
            landcolor='rgb(204, 204, 204)',
            countrycolor='rgb(204, 204, 204)',
            lakecolor='rgb(255, 255, 255)',
            # projection_type="equirectangular",
            # coastlinewidth=2,
            # lataxis=dict(
            #     range=[20, 60],
            #     showgrid=True,
            #     dtick=10
            # ),
            # lonaxis=dict(
            #     range=[-100, 20],
            #     showgrid=True,
            #     dtick=20
            # ),
        ),

        # # Add buttons to be able to choice the shown data #
        # updatemenus=[
        #     {
        #         "buttons": [
        #             {
        #                 "label": f"{m}",
        #                 "method": "update",
        #                 "args": [
        #                     {
        #                         "visible": [
        #                             (m2 == m)
        #                             for m2 in maps_titles
        #                         ]
        #                     },
        #                     {"title": f"<b>{m}</b>"},
        #                 ],
        #             }
        #             for m in maps_titles
        #         ],
        #         "type": "dropdown",
        #         "direction": "right",
        #         "x": 0.18,
        #         "pad": {"l": 0, "r": 0, "t": 25, "b": 0},
        #     },
        # ],
        margin={"l": 0, "r": 0, "t": 75, "b": 0},
        # paper_bgcolor="black",
        clickmode="event+select",
        # transition_easing="elastic-in-out",
        # datarevision=1
        # bargap=1
    )

    return fig, groups_index, bars_fig


def generate_table(dataframe):  #, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns])
            for i in range(len(dataframe))
            # for i in range(min(len(dataframe), max_rows))
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

    # return fig


def change_frame(fig, slider, frame_number=np.NaN, frame_name=''):
    if np.isnan(frame_number) or frame_name == '':
        frame_number = slider['active']
        frame_name = slider['steps'][slider['active']]['args'][0][0]

    fig.layout.sliders[0].active = frame_number

#     # fig.update_traces(z=fig.frames[frame_number].data[0].z)     # frame_number=-1 - last

    fig.data[0].update(fig.frames[frame_number].data[0])

    # fig.data[0].z = fig.frames[frame_number].data[0].z
    # fig.data[0].customdata = fig.frames[frame_number].data[0].customdata
    # fig.data[0].hovertext = fig.frames[frame_number].data[0].hovertext
    # fig.data[0].locations = fig.frames[frame_number].data[0].locations
#
#     # fig.update_traces(frame=dict(duration=500, redraw=False), selector=dict(type='choropleth'))
#     # fig.update_traces(frame=dict(value=frame_number))
#     # fig['layout']['sliders'][0]['active'] = frame_number
#
    # fig.update_layout(
    #     sliders=[
    #         dict(
    #             borderwidth=2,
    #             # active=frame_number,
    #             steps=[dict(#method="animate",
    #                         args=[[frame_name]#,
    #                               # {
    #                               #  "frame": {"duration": 1000, "redraw": True},
    #                               #  "fromcurrent": True,
    #                               #  'transition': {'duration': 300}
    #                               #  }
    #                               ]
    #                         )
    #                    ],
    #         )
    #     ]
    # )
#
#     # fig.update_layout(
#     #     updatemenus=[
#     #         dict(
#     #             active=frame_number,
#     #         )
#     #     ]
#     # )
#
    # return fig
