import pandas as pd
from dash import html
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html
from dash.dash_table import DataTable

from assets.config import Config
from src.load_data import distinguish_data

config = Config()


def generate_project_deep_dive_visualisation(df: pd.DataFrame):
    table_fig = generate_table_data(df.copy())

    return table_fig


def generate_table_data(df: pd.DataFrame,
                        council: str = config.default_council) -> DataTable:
    df.columns = df.columns.droplevel(0)
    df.columns = df.columns.droplevel(0)

    df = df[df['Organisations'] == council]

    table = DataTable(
        columns=[{"name": col, "id": col} for col in df.columns[1:]],
        data=df.to_dict('records'),
        page_size=20,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={'fontWeight': 'bold'},
    )
    return table


def update_dash5_visuals_func(df, council):
    table_fig = generate_table_data(df.copy(), council)

    return table_fig
