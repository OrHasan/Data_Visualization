from dash import dcc, html
# - - - - - - - - - - - - - - -
from Code import functions as func


def show_data(attacks_data, connections):
    return html.Div(children=[
        html.Label('Country'),
        dcc.Dropdown(list(set(attacks_data['Country'])),
                     attacks_data['Country'][0],
                     clearable=False,
                     id='Show_Country'),

        html.Br(),
        html.Label('Group'),
        dcc.Dropdown(attacks_data['Groups '][0].split(', '),
                     attacks_data['Groups '][0].split(', ')[0],
                     clearable=False,
                     id='Show_Group'),

        html.Br(),
        html.Label('Connected Groups'),
        dcc.Dropdown(['BlaBla', 'BliBla'],
                     ['BlaBla'],
                     multi=True,
                     clearable=False,
                     disabled=True,
                     id='Show_Connections'),

        html.Br(),
        html.H4(children='Map Database'),
        func.generate_table(attacks_data),

        html.Div(children=[
            html.Br(),
            html.H4(children='Map Database'),
            func.generate_table(connections) if not connections.empty else None
        ], style={'display': 'block' if not connections.empty else 'none'})

    ], style={'padding': 10, 'display': 'block'}, id='Show_Data')


def new_country(attacks_data):
    return html.Div(children=[
        html.Label('Country Name'),
        html.Br(),
        dcc.Input(type='text'),

        html.Br(), html.Br(),
        html.Label('Groups Names'),
        html.Br(),
        dcc.Input(type='text'),

        html.Br(),
        html.H4(children='Map Database'),
        func.generate_table(attacks_data),
    ], style={'padding': 20, 'display': 'none'}, id='New_Country')


def new_groups(connections):
    return html.Div(children=[
        html.Label('Group Name'),
        html.Br(),
        dcc.Input(type='text'),

        html.Br(), html.Br(),
        html.Label('Group Connection'),
        html.Br(),
        dcc.Input(type='text'),

        html.Div(children=[
            html.Br(),
            html.H4(children='Map Database'),
            func.generate_table(connections) if not connections.empty else None
        ], style={'display': 'block' if not connections.empty else 'none'})

    ], style={'padding': 20, 'display': 'none'}, id='New_Groups')


def threat_level():
    return html.Div(children=[
        html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),
        html.Label('Threat Level'),
        dcc.Slider(
            min=1,
            max=5,
            step=1,
            marks={1: {'label': '1', 'style': {'color': '#00CC00'}},  # RRGGBB
                   2: {'label': '2', 'style': {'color': '#00AA00'}},
                   3: {'label': '3', 'style': {'color': '#888800'}},
                   4: {'label': '4', 'style': {'color': '#AA0000'}},
                   5: {'label': '5', 'style': {'color': '#CC0000'}}
                   },
            value=2,
            dots=True,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
    ], style={'padding': 10, 'flex': 1})


def db_update(attacks_data, connections, date_animation):
    return html.Div(children=[
        # html.Div(children=[
        dcc.Store(id='UI_Visibility',
                  data={'Show_Data_Visible': True,
                        'New_Country_Visible': False,
                        'New_Groups_Visible': False,
                        'Tab': 'Show_Map',
                        'map_current_style': 'kavrayskiy7',
                        'map_animation': date_animation,
                        }),

        html.Div(children=[
            html.Label('Function'),
            dcc.RadioItems(options=[
                {'label': 'Show Data by Country', 'value': 'Show Data'},
                {'label': 'Add New Country', 'value': 'Add Country'},
                {'label': 'Add New Groups', 'value': 'Add Groups'}
            ],
                value='Show Data',
                id='UI_State', ),
            html.Br(),

            show_data(attacks_data, connections),
            new_country(attacks_data),
            new_groups(connections),

            html.Br(),
            html.Button('Update Database',
                        id='update',
                        n_clicks=0,
                        disabled=True),
        ], style={'padding': 10, 'flex': 3}),

        threat_level()

        # ], style={'display': 'flex', 'flexDirection': 'row'})
    ], style={'display': 'none', 'flexDirection': 'row'}, id='Update_DB')
