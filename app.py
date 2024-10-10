from dash import Dash, html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import os

from src.dash1 import generate_project_visualisation as viz1, update_dash1_visuals_func
from src.dash2 import generate_project_classification_visualizations as viz2, update_dash2_visuals_func, update_project_classification_overview_fig
from src.dash3 import generate_project_value_distribution_visualisation as viz3, update_dash3_visuals_func, get_max_project_value, update_project_value_overview_fig
from src.dash4 import generate_project_theme_distribution_visualisation as viz4, update_dash4_visuals_func
from src.dash5 import generate_project_deep_dive_visualisation as viz5, update_dash5_visuals_func

from src.load_data import preprocess_data, get_project_classification

from assets.config import Config

config = Config()

title = "Project List Dashboard"

# Read in data
print('Reading data...')
curr_path = os.getcwd()
data_path = os.path.join(curr_path, 'Project List.xlsx')
raw_data = preprocess_data(data_path)

# Initialize the app
print("Initialise app...")
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='Nottingham Project List Dashboard',
    suppress_callback_exceptions=True,
    prevent_initial_callbacks='initial_duplicate')
server = app.server


# Dropdown for council
council_dropdown = html.Div(
    [
        dbc.Label("Select a Council", html_for="council_dropdown"),
        dcc.Dropdown(
            id="council-dropdown",
            options=sorted(raw_data[('Fast Followers member', 'Unnamed: 0_level_1', 'Organisations')].unique()),
            value=config.default_council,
            clearable=False,
            style={'marginBottom': '5px'}
        ),
    ]
)


# Dropdown for project classification
project_classification_dropdown = html.Div(
    children=[
        html.Label("Pick a Classification"),
        html.Div(
            children=dcc.Checklist(
                id="project-classification-checklist",
                options=[{"label": "Select All Classification", "value": "All"}],
                value=[],
            ),
        ),
        html.Div(
            children=dcc.Dropdown(
                id="project-classification-dropdown",
                options=get_project_classification(raw_data.copy()),
                value=get_project_classification(raw_data.copy()),
                multi=True,
                searchable=True,
            ),
        ),
    ],
)


# Slider for project value
project_value_slider = html.Div(
    children=[
        html.Label("Project Value Slider"),
        html.Div(
            children=dcc.RangeSlider(
                id="project-value-slider",
                min=0,
                max=get_max_project_value(raw_data.copy()),
                value=[0, get_max_project_value(raw_data.copy())],
                tooltip={"placement": "bottom", "always_visible": True},
                allowCross=False,
            ),
        )
    ],
)


app.layout = html.Div([
    dbc.Container([
        dbc.Row(html.H1(
            children=title,
            style={'textAlign': 'center', 'paddingTop': '20px',
                   'color': config.secondary_color})),
        dbc.Row(dcc.Tabs(id='graph-tabs', value='project_count', children=[
                    dcc.Tab(label='Projects', value='project_count',
                            style=config.tab_style['idle'],
                            selected_style=config.tab_style['active']),
                    dcc.Tab(label='Project Classification', value='project_classification',
                            style=config.tab_style['idle'],
                            selected_style=config.tab_style['active']),
                    dcc.Tab(label='Project Value Distribution', value='project_value_distribution',
                            style=config.tab_style['idle'],
                            selected_style=config.tab_style['active']),
                    dcc.Tab(label='Project Theme Distribution', value='project_theme_distribution',
                            style=config.tab_style['idle'],
                            selected_style=config.tab_style['active']),
                    dcc.Tab(label='Project Deep Dive', value='project_deep_dive',
                            style=config.tab_style['idle'],
                            selected_style=config.tab_style['active']),
                ], style={'paddingTop': '10px', 'paddingBottom': '5px',
                          'height': '50vx'})),
        dbc.Row([
            dcc.Tabs(id='tabs', value='overview', children=[
                dcc.Tab(label='Overview', value='overview',
                        style={'border': '1px line white',
                               'backgroundColor': config.secondary_color,
                               'color': config.primary_color,
                               'fontWeight': 'bold'},
                        selected_style={'border': '1px solid white',
                                        'backgroundColor': config.secondary_color,
                                        'color': config.primary_color,
                                        'fontWeight': 'bold',
                                        'textDecoration': 'underline'}),
                dcc.Tab(label='Council View', value='council_view',
                        style={'border': '1px solid white',
                               'backgroundColor': config.secondary_color,
                               'color': config.primary_color,
                               'fontWeight': 'bold'},
                        selected_style={'border': '1px solid white',
                                        'backgroundColor': config.secondary_color,
                                        'color': config.primary_color,
                                        'fontWeight': 'bold',
                                        'textDecoration': 'underline'}),
            ], style={'paddingTop': '10px', 'paddingBottom': '15px'})
        ]),
        dbc.Row([
            dcc.Loading([
                html.Div(id='tabs-content')
            ], type='default', color=config.primary_color)
        ])
    ], style={'padding': '0px'})
], style={'backgroundColor': 'white', 'minHeight': '100vh'})


# Update dash 1
@app.callback(
    Output("project-count-card", "children"),
    Output('project-count-graph1', 'figure'),
    Output('project-count-graph2', 'children'),
    Input("council-dropdown", "value")
)
def update_dash1_visuals(council):
    return update_dash1_visuals_func(raw_data.copy(), council)


# Update dash 2
@app.callback(
    Output("project-classification-graph1", "figure"),
    Output('project-classification-graph2', 'figure'),
    Input("council-dropdown", "value")
)
def update_dash2_visuals(council):
    return update_dash2_visuals_func(raw_data.copy(), council)


# Update dash 3
@app.callback(
    Output("project-value-distribution-graph1", "figure"),
    Input("council-dropdown", "value")
)
def update_dash3_visuals(council):
    return update_dash3_visuals_func(raw_data.copy(), council)


# Update dash 4
@app.callback(
    Output("project-theme-distribution-graph1", "figure"),
    Input("council-dropdown", "value")
)
def update_dash4_visuals(council):
    return update_dash4_visuals_func(raw_data.copy(), council)


# Update dash 5
@app.callback(
    Output("project-deep-dive-graph1", "children"),
    Input("council-dropdown", "value")
)
def update_dash5_visuals(council):
    return update_dash5_visuals_func(raw_data.copy(), council)


# Project classification overview
@app.callback(
    Output("project-classification-dropdown", "value"),
    Output("project-classification-graph1", "figure", allow_duplicate=True),
    [Input("project-classification-checklist", "value"),
     Input("project-classification-dropdown", "value")]
)
def update_classification_dropdown(select_all, select_some):
    if select_all == ["All"]:
        value = get_project_classification(raw_data.copy())
    else:
        value = no_update

    fig = update_project_classification_overview_fig(
        raw_data.copy(), select_some, select_all)

    return value, fig


# Project value distribution overview
@app.callback(
    Output("project-value-distribution-graph1", "figure", allow_duplicate=True),
    Input("project-value-slider", "value")
)
def update_classification_dropdown(slider_value):
    fig = update_project_value_overview_fig(raw_data.copy(), slider_value)

    return fig

# @app.callback(
#     Output("checklist-container", "children"),
#     [Input("region-select", "value")],
#     [State("region-select", "options"), State("region-select-all", "value")],
# )
# def update_checklist(selected, select_options, checked):
#     if len(selected) < len(select_options) and len(checked) == 0:
#         raise PreventUpdate()
#
#     elif len(selected) < len(select_options) and len(checked) == 1:
#         return dcc.Checklist(
#             id="region-select-all",
#             options=[{"label": "Select All Regions", "value": "All"}],
#             value=[],
#         )
#
#     elif len(selected) == len(select_options) and len(checked) == 1:
#         raise PreventUpdate()
#
#     return dcc.Checklist(
#         id="region-select-all",
#         options=[{"label": "Select All Regions", "value": "All"}],
#         value=["All"],
#     )


@app.callback(
    Output('tabs-content', 'children'),
    [Input('graph-tabs', 'value'),
    Input('tabs', 'value')]
)
def update_tab(tab, tab2):
    if tab == 'project_count':
        fig_card, fig_bar, fig_donut, table_fig = viz1(raw_data.copy(), tab2)
        if tab2 == "overview":
            return html.Div([
                fig_card,
                html.Div([
                    dcc.Graph(id='project-count-graph1', figure=fig_bar),
                ], style={'width': '100%', 'paddingTop': '20px',
                          'paddingBottom': '20px',
                          'display': 'inline-block'})
            ])
        else:
            return html.Div([
                dbc.Col([council_dropdown]),
                fig_card,
                html.Div([
                    dcc.Graph(id='project-count-graph1', figure=fig_donut),
                ], style={'width': '50%', 'paddingTop': '20px',
                          'paddingBottom': '5px', 'margin': 'auto'}),
                html.Div([
                    table_fig,
                ], id="project-count-graph2", style={'width': '100%'}),
            ])
    elif tab == 'project_classification':
        fig1, donut_fig = viz2(raw_data.copy(), tab2)

        if tab2 == "overview":
            return html.Div([
                dbc.Col([project_classification_dropdown]),
                html.Div([
                    dcc.Graph(id='project-classification-graph1', figure=fig1),
                ], style={'width': '100%', 'display': 'inline-block',
                          'height': '150vh', 'paddingTop': '20px'}),
            ])
        else:
            return html.Div([
                dbc.Col([council_dropdown]),
                html.Div([
                    dcc.Graph(id='project-classification-graph1', figure=fig1),
                ], style={'width': '60%', 'paddingTop': '20px',
                          'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='project-classification-graph2',
                              figure=donut_fig),
                ], style={'width': '40%', 'paddingTop': '20px',
                          'paddingBottom': '5px',
                          'display': 'inline-block'}),
            ])
    elif tab == 'project_value_distribution':
        fig_bar = viz3(raw_data.copy(), tab2)

        if tab2 == 'overview':
            return html.Div([
                dbc.Col([project_value_slider]),
                html.Div([
                    dcc.Graph(id='project-value-distribution-graph1', figure=fig_bar),
                ], style={'width': '100%', 'paddingTop': '20px'}),
            ])
        else:
            return html.Div([
                dbc.Col([council_dropdown]),
                html.Div([
                    dcc.Graph(id='project-value-distribution-graph1',
                              figure=fig_bar),
                ], style={'width': '100%', 'paddingTop': '20px'}),
            ])
    elif tab == 'project_theme_distribution':
        fig_bar = viz4(raw_data.copy(), tab2)

        if tab2 == "overview":
            return html.Div([
                html.Div([
                    dcc.Graph(id='project-theme-distribution-graph1', figure=fig_bar),
                ], style={'width': '100%', 'paddingTop': '20px'}),
            ])
        else:
            return html.Div([
                dbc.Col([council_dropdown]),
                html.Div([
                    dcc.Graph(id='project-theme-distribution-graph1', figure=fig_bar),
                ], style={'width': '100%', 'paddingTop': '20px'}),
            ])
    elif tab == 'project_deep_dive':
        table_fig = viz5(raw_data.copy(), tab2)

        if tab2 == "overview":
            return html.Div([
                    table_fig,
                ], id="project-deep-dive-graph1", style={'width': '100%'})
        else:
            return html.Div([
                dbc.Col([council_dropdown]),
                html.Div([
                    table_fig,
                ], id="project-deep-dive-graph1", style={'width': '100%'}),
            ])


if __name__ == '__main__':
    app.run(debug=True)




