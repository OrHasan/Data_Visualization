from dash import Dash, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# - - - - - - - - - - - - - - -
import html_graphs_divisions as graph_division
import html_db_tab_divisions as db_tab_division
import event_listener as event


def set_server(attacks_data, fig, bars_fig, connections, date_animation):
    event.init(attacks_data)

    app = Dash(__name__)

    app.layout = html.Div([
        # # Add drop-list #
        # dcc.Dropdown(
        #     id='dropdown',
        #     options=[
        #         {'label': maps_titles[0], 'value': maps_titles[0]},
        #         {'label': maps_titles[1], 'value': maps_titles[1]},
        #     ],
        #     value='NYC'
        # ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Attack Groups")),
                dbc.ModalBody(id="modal-body"),
                # dbc.ModalFooter(
                #     dbc.Button(
                #         "Close", id="CloseModal", className="ms-auto", n_clicks=0
                #     )
                # ),
            ],
            id="Country_Info_Popup",
            scrollable=True,
            is_open=False,
        ),

        html.Button('Update Database Page',
                    n_clicks=0,
                    id='Update_Database',
                    style={'font-size': 12.5, 'width': 100}),
                    # style={'display': 'flex', 'margin': '0 auto'}),

        graph_division.map_view(fig, bars_fig, date_animation),
        db_tab_division.db_update(attacks_data, connections, date_animation)
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
    app.callback(
        Output('choropleth', 'style'),
        Output('bars', 'style'),
        Output('choropleth', 'figure', allow_duplicate=True),
        # Output('UI_Visibility', 'data', allow_duplicate=True),
        Input('data_view', 'value'),
        State('choropleth', 'figure'),
        # State('UI_Visibility', 'data'),
        prevent_initial_call=True
    )(event.change_figure)
    # def change_figure(data_view, fig):
    #     map_display, bars_display, fig = event.change_figure(data_view, fig)
    #     return map_display, bars_display, fig    #, store_data

    # # core update of figure on change of dash slider #
    # @app.callback(
    #     Output('whichframe', 'children'),
    #     # Output('choropleth', 'figure', allow_duplicate=True),
    #     Input('sliderInterval', 'n_intervals'),
    #     State('choropleth', 'figure'),
    #     State('UI_Visibility', 'data'),
    #     prevent_initial_call=True
    # )
    # def set_frame(n_intervals, fig, store_data):
    #     text = event.set_frame(n_intervals, fig, store_data, screensize, color_axis)
    #     slider, pos_name = event.set_frame(n_intervals, fig, store_data, screensize, color_axis)
    #     # return text
    #     # return f"active:{slider['active']} value:{pos_name}"

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

    # @app.callback(
    #     # Output('choropleth', 'figure', allow_duplicate=True),
    #     Output('whichframe', 'children'),
    #     Input('choropleth', 'relayoutData'),
    #     # State('choropleth', 'figure'),
    #     State('UI_Visibility', 'data'),
    #     prevent_initial_call=True
    # )
    # def set_frame(relayout_data, store_data):
    #     fig = event.set_frame(relayout_data, store_data, screensize, color_axis)
    #     # return fig

    # Click event - country selection #
    if not connections.empty:
        @app.callback(
            Output('choropleth', 'figure'),
            Output("Country_Info_Popup", "is_open"),
            Output("modal-body", "children"),
            Input('choropleth', 'clickData'),
            State('choropleth', 'figure'),
            State('UI_Visibility', 'data'),
            State("Country_Info_Popup", "is_open"),
            prevent_initial_call=True)
        def update_figure(click_data, fig, store_data, is_open):
            fig, is_open, modal_body = event.update_figure(click_data, fig, store_data, connections, screensize,
                                                           color_axis, data_by_attacks, is_open)
            return fig, is_open, modal_body
            # return get_figure(selections)

    else:
        @app.callback(
            Output("Country_Info_Popup", "is_open"),
            Output("modal-body", "children"),
            Input('choropleth', 'clickData'),
            State('choropleth', 'figure'),
            State('UI_Visibility', 'data'),
            State("Country_Info_Popup", "is_open"),
            prevent_initial_call=True)
        def update_figure(click_data, fig, store_data, is_open):
            _, is_open, modal_body = event.update_figure(click_data, fig, store_data, connections, screensize,
                                                         color_axis, data_by_attacks, is_open)
            # print(is_open)
            return is_open, modal_body
            # return get_figure(selections)

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
    # def update_tab(n_clicks, store_data):
    #     store_data, button_text, Map_display, Update_display = event.update_tab(n_clicks, store_data)
    #     return store_data, button_text, Map_display, Update_display

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
    # def toggle_dropdown(selected_option, store_data):
    #     Show_Data_display, New_Country_display, New_Groups_display, store_data = event.toggle_dropdown(selected_option,
    #                                                                                                    store_data)
    #
    #     return Show_Data_display, New_Country_display, New_Groups_display, store_data

    # Change visible elements in Update Database tab while changing the country #
    app.callback(
        Output('Show_Group', 'options'),
        Output('Show_Group', 'value'),
        # Output('Show_Connections', 'options'),
        # Output('Show_Connections', 'value'),
        Input('Show_Country', 'value'),
        prevent_initial_call=True
    )(event.update_groups)
    # def update_groups(selected_country):
    #     groups_options, groups_value = event.update_groups(selected_country)
    #     return groups_options, groups_value
