import pandas as pd
import plotly.express as px

from assets.config import Config
from src.load_data import distinguish_data

config = Config()


def generate_project_theme_distribution_visualisation(df: pd.DataFrame, tab: str):
    df_cleaned = clean_data(df)
    df_council_project_theme = distinguish_data(tab, df_cleaned)

    fig = generate_bar_graph(df_council_project_theme, tab)

    return fig


def generate_bar_graph(df, tab):
    if tab == 'overview':
        max_value = len(set(df['Organisations']))
        fig_height = max(600, max_value * 40)

        fig = px.bar(
            df,
            x="Theme count",
            y="Organisations",
            color="Theme",
            title="Theme Count Per Council",
            height=fig_height
        )

    else:
        max_value = len(set(df['Theme count']))
        fig_height = max(600, max_value * 40)

        fig = px.bar(
            df,
            x="Theme",
            y="Theme count",
            title="Council Projects Theme Distribution",
            height=fig_height,
            color_discrete_sequence=[config.primary_color] * len(df)
        )
    return fig


def clean_data(df: pd.DataFrame):
    df_council_project_theme = df.droplevel(level=[0, 1], axis=1)

    df_council_project_theme = df_council_project_theme[
        ['Organisations', 'Theme']]

    theme_mapping = {
        "EV Infastructure": "EV Infrastructure",
        "Heat": "Heating",
        "Heating ": "Heating",
        "Retrofit ": "Retrofit",
        'Transport/Alternative Fuels': 'Transport and Alternative Fuels',
        'retrofit': "Retrofit",
        'retrofit ': "Retrofit"
    }

    df_council_project_theme['Theme'] = df_council_project_theme[
        'Theme'].apply(lambda x: theme_mapping[x] if x in theme_mapping else x)

    df_council_project_theme['Theme count'] = \
        df_council_project_theme.groupby(['Organisations', 'Theme'])[
            'Theme'].transform('count')

    return df_council_project_theme.drop_duplicates()


def update_dash4_visuals_func(df, council):
    df_cleaned = clean_data(df)
    df_council_project_theme = distinguish_data("council_view", df_cleaned, council)

    fig = generate_bar_graph(df_council_project_theme, "council_view")

    return fig
