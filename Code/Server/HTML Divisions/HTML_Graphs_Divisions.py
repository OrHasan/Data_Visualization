from dash import dcc, html


def top_menu(date_animation):
    return html.Div(children=[
        html.Div(children=[
            html.Label('Map Style'),
            dcc.Dropdown(['2D', '3D'],
                         '2D',
                         clearable=False,
                         id='map_style'),
        ], style={'width': '7%', 'margin': '0 auto', 'textAlign': 'center'}),

        html.Div(children=[
            html.Label('Map Style'),
            dcc.Dropdown(['Map View', 'Bars View'],
                         'Map View',
                         clearable=False,
                         id='data_view'),
        ], style={'width': '10%', 'margin': '0 auto', 'textAlign': 'center'}),

        html.Div(children=[
            html.Label('Selected Data'),
            dcc.Dropdown([{'label': 'By Date', 'value': 'By Date', 'disabled': not date_animation},
                          {'label': 'Summarized', 'value': 'Summarized'}],
                         'By Date' if date_animation else 'Summarized',
                         clearable=False,
                         id='map_data'),
        ], style={'width': '13%', 'margin': '0 auto', 'textAlign': 'center'}),
    ], style={'display': 'flex'})


def map_view(fig, bars_fig, date_animation):
    return html.Div(children=[
        top_menu(date_animation),

        # html.Div(children=[
        dcc.Loading(
            # Add the map-graph #
            dcc.Graph(
                id='choropleth',
                figure=fig,
            ),
            type="graph",
            # style={'flex-grow': '1', 'width': '90%', 'height': '100vh'}
            # debug=True
        ),

        # style={'flex-basis': '10%'}),

        # Add the bar-graph #
        dcc.Graph(
            id='bars',
            figure=bars_fig,
            style={'display': 'none'}
        ),

        dcc.Interval(
            id="sliderInterval",
            interval=400,
        ),

        html.Div(
            id="whichframe",
            children=[]
        )
    ], style={'display': 'block'}, id='Map_View')
