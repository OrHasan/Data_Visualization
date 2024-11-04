from dash import Dash, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# - - - - - - - - - - - - - - -
# please ignore if the IDE marks the 2 following lines as missing, there paths are loaded in "main.py"
import html_graphs_divisions as graph_division
import html_db_tab_divisions as db_tab_division
import event_listener as event


def set_server(attacks_data, fig, bars_fig, connections, date_animation, db_location):
    global map_dropdown_style
    map_dropdown_style = {'width': '13%', 'margin': '0 auto', 'textAlign': 'center'}

    event.init(attacks_data)

    app = Dash('__main__')

    app.layout = html.Div([
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                dbc.ModalBody(id="modal-body"),
            ],
            id="Country_Info_Popup",
            scrollable=True,
            is_open=False,
        ),

        html.Button('Change Database',
                    n_clicks=0,
                    id='Update_Database',
                    style={'font-size': 12.5, 'width': 100}),

        graph_division.map_view(fig, bars_fig, date_animation, map_dropdown_style),
        db_tab_division.db_update(attacks_data, connections, date_animation, db_location)
    ])

    return app


def events(app, attacks_data, attacks_sum, screensize, color_axis, connections, data_by_attacks):
    # Choice between 2D & 3D map visuality #
    @app.callback(
        Output('choropleth', 'figure', allow_duplicate=True),
        Output('UI_Visibility', 'data', allow_duplicate=True),
        Input('map_style', 'value'),
        State('choropleth', 'figure'),
        State('UI_Visibility', 'data'),
        prevent_initial_call=True
    )
    def change_map_style(map_style, fig, store_data):
        fig, store_data = event.change_map_style(map_style, fig, store_data, screensize, color_axis, data_by_attacks)
        return fig, store_data

    # Choice between Timeline & Summary map visuality #
    @app.callback(
        Output('choropleth', 'figure', allow_duplicate=True),
        Output('UI_Visibility', 'data', allow_duplicate=True),
        Input('map_data', 'value'),
        State('choropleth', 'figure'),
        State('UI_Visibility', 'data'),
        prevent_initial_call=True
    )
    def change_map_data(map_data, fig, store_data):
        fig, store_data = event.change_map_data(map_data, fig, store_data, attacks_data, attacks_sum, screensize,
                                                color_axis, data_by_attacks)
        return fig, store_data

    # Choice the graph type #
    @app.callback(
        Output('map_style_display', 'style'),
        Output('map_data_display', 'style'),
        Output('choropleth', 'style'),
        Output('bars', 'style'),
        Output('choropleth', 'figure', allow_duplicate=True),
        Input('data_view', 'value'),
        State('choropleth', 'figure'),
        prevent_initial_call=True
    )
    def figure_type(data_view, fig):
        global map_dropdown_style
        map_style_dropdown, map_data_dropdown, map_display, bars_display, fig =\
            event.change_figure(data_view, fig, map_dropdown_style)
        return map_style_dropdown, map_data_dropdown, map_display, bars_display, fig

    # TEST #
    @app.callback(
        Output('whichframe', 'children', allow_duplicate=True),
        Output('choropleth', 'figure', allow_duplicate=True),
        Input('whichframe', 'children'),
        State('choropleth', 'figure'),
        State('UI_Visibility', 'data'),
        prevent_initial_call=True
    )
    def init_connections(n_intervals, fig, store_data):
        event.init_connections(n_intervals, fig, store_data, screensize, color_axis, data_by_attacks)
        return ""

    # Click event - country selection #
    if not connections.empty:
        @app.callback(
            Output('choropleth', 'figure'),
            Output("Country_Info_Popup", "is_open"),
            Output("modal-title", "children"),
            Output("modal-body", "children"),
            Input('choropleth', 'clickData'),
            State('choropleth', 'figure'),
            State('UI_Visibility', 'data'),
            State("Country_Info_Popup", "is_open"),
            prevent_initial_call=True)
        def update_figure(click_data, fig, store_data, is_open):
            fig, is_open, modal_title, modal_body = event.update_figure(click_data, fig, store_data, connections,
                                                                        screensize, color_axis, data_by_attacks,
                                                                        is_open)
            return fig, is_open, modal_title, modal_body

    else:
        @app.callback(
            Output("Country_Info_Popup", "is_open"),
            Output("modal-title", "children"),
            Output("modal-body", "children"),
            Input('choropleth', 'clickData'),
            State('choropleth', 'figure'),
            State('UI_Visibility', 'data'),
            State("Country_Info_Popup", "is_open"),
            prevent_initial_call=True)
        def update_figure(click_data, fig, store_data, is_open):
            _, is_open, modal_title, modal_body = event.update_figure(click_data, fig, store_data, connections,
                                                                      screensize, color_axis, data_by_attacks,
                                                                      is_open)
            return is_open, modal_title, modal_body

    # Choice the visible Tab #
    app.callback(
        Output('UI_Visibility', 'data', allow_duplicate=True),
        Output('Update_Database', 'children'),
        Output('Map_View', 'style'),
        Output('Update_DB', 'style'),
        Input('Update_Database', 'n_clicks'),
        State('UI_Visibility', 'data'),
        prevent_initial_call=True
    )(event.update_tab)

    # Change visible elements in Update Database tab while changing the dropdown value #
    app.callback(
        Output('Show_Data', 'style'),
        Output('New_Country', 'style'),
        Output('New_Groups', 'style'),
        Output('UI_Visibility', 'data'),
        Input('UI_State', 'value'),
        State('UI_Visibility', 'data'),
        prevent_initial_call=True
    )(event.toggle_dropdown)

    # Change visible elements in Update Database tab while changing the country #
    app.callback(
        Output('Show_Group', 'options'),
        Output('Show_Group', 'value'),
        Input('Show_Country', 'value'),
        prevent_initial_call=True
    )(event.update_groups)
