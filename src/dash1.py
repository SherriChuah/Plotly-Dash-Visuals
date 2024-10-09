import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html
from dash.dash_table import DataTable

from assets.config import Config
from src.load_data import distinguish_data

config = Config()


def generate_project_visualisation(df: pd.DataFrame, tab: str):
    df_cleaned = clean_data(df)
    df_council_and_projects = distinguish_data(tab, df_cleaned)

    df_council_and_projects = df_council_and_projects.drop_duplicates()

    value = len(list(df_council_and_projects['Project Name']))
    fig_card = generate_stats_card("Project Count", value)

    if tab == "overview":
        fig_bar = generate_bar_chart(df_council_and_projects)
        fig_table = None
        fig_donut = None
    else:
        fig_donut = generate_donut_chart(df_council_and_projects)
        fig_table = generate_table_data(df.copy())
        fig_bar = None

    return fig_card, fig_bar, fig_donut, fig_table


def clean_data(df: pd.DataFrame):
    df_council_and_projects = df.droplevel(level=[0, 1], axis=1)

    df_council_and_projects = df_council_and_projects[
        ['Organisations', 'Project Name']]

    return df_council_and_projects


def generate_stats_card(title, value):
    return html.Div(
        dbc.Card([
            dbc.CardBody([
                html.H4(title, className="card-title",
                        style={'margin': '0px', 'fontSize': '18px',
                               'fontWeight': 'bold'}),
                html.P(value, className="card-value",
                       style={'margin': '0px', 'fontSize': '22px',
                              'fontWeight': 'bold'}),
            ], style={'textAlign': 'center'}),
        ], style={'paddingBlock': '10px', "backgroundColor": config.primary_color,
                  'border': 'none', 'borderRadius': '10px'}),
        id='project-count-card'
    )


def generate_bar_chart(df):
    df["Project Counts"] = df.groupby(['Organisations'])['Project Name'].transform('count')

    df = df[['Organisations', 'Project Counts']]
    df = df.drop_duplicates()

    df = df.sort_values(['Project Counts'], ascending=True)

    max_value = len(set(df['Organisations']))
    fig_height = max(700, max_value * 40)

    fig = px.bar(
        df,
        x="Project Counts",
        y="Organisations",
        title="Project Count Per Council",
        height=fig_height,
        color_discrete_sequence=[config.primary_color] * len(df)
    )
    return fig


def generate_donut_chart(df):
    label = list(df['Project Name'])

    parents = list(df['Organisations'])

    fig = go.Figure(go.Sunburst(
        labels=label,
        parents=parents,
        branchvalues="total"))

    fig.update_layout(title='Council Project Names',
                      margin=dict(t=30, l=10, r=10, b=0))

    return fig


def generate_table_data(df: pd.DataFrame, council: str = config.default_council) -> DataTable:
    df.columns = df.columns.droplevel(0)
    df.columns = df.columns.droplevel(0)

    df = df[df['Organisations'] == council]

    table = DataTable(
            columns=[{"name": col, "id": col} for col in df.columns[1:]],
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'fontWeight': 'bold'},
        )
    return table


def update_dash1_visuals_func(df, council):
    df_cleaned = clean_data(df)
    df_council_and_projects = distinguish_data('council_view', df_cleaned, council)
    df_council_and_projects = df_council_and_projects.drop_duplicates()

    value = len(list(df_council_and_projects['Project Name']))
    fig_card = generate_stats_card("Project Count", value)

    table_fig = generate_table_data(df, council)

    return fig_card, generate_donut_chart(df_council_and_projects), table_fig
