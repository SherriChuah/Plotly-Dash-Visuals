import pandas as pd
import plotly.express as px

from assets.config import Config
from src.load_data import distinguish_data

config = Config()


def generate_project_value_distribution_visualisation(df: pd.DataFrame, tab: str):
    df_project_distribution_value = clean_data(df.copy())

    df_project_distribution_value = distinguish_data(tab, df_project_distribution_value)

    fig_bar = generate_bar_graph(df_project_distribution_value)

    return fig_bar


def clean_data(df: pd.DataFrame):
    df = df.droplevel(level=[0, 1], axis=1)
    df = df.iloc[:, :3]
    df = df.fillna(0)

    # Filter off rows with non int Project value
    df_project_distribution_value = df[
        ~(df["Project Value"].apply(
            lambda x: isinstance(x, str)))]

    df_project_distribution_value["Project Value"] = (
        df_project_distribution_value["Project Value"].astype(int))

    df_project_distribution_value = (
        df_project_distribution_value.sort_values(
            by=['Project Value'], ascending=[True]))

    return df_project_distribution_value


def generate_bar_graph(df):
    max_value = len(set(df['Project Name']))
    fig_height = max(1100, max_value * 40)

    fig_bar = px.bar(
        df,
        x="Project Value",
        y="Project Name",
        height=fig_height,
        title="Project Value Distribution",
        color_discrete_sequence=[config.primary_color] * len(df)
    )

    fig_bar.update_layout(
        yaxis=dict(
            tickvals=df['Project Name'],
            ticktext=[wrap_label(label) for label in df['Project Name']]
        ))

    return fig_bar


def wrap_label(label):
    words = label.split()
    wrapped = []

    for i in range(0, len(words), 7):
        wrapped.append(' '.join(words[i:i + 7]))

    return '<br>'.join(wrapped)


def update_dash3_visuals_func(df, council):
    df_project_distribution_value = clean_data(df.copy())

    df_project_distribution_value = distinguish_data(
        'council_view', df_project_distribution_value, council)

    fig_bar = generate_bar_graph(df_project_distribution_value)

    return fig_bar


def get_max_project_value(df):
    df = df.droplevel(level=[0, 1], axis=1)
    df = df.iloc[:, :3]
    df = df.fillna(0)

    df_project_distribution_value = df[
        ~(df["Project Value"].apply(
            lambda x: isinstance(x, str)))]

    df_project_distribution_value.loc[:, "Project Value"] = (
        df_project_distribution_value["Project Value"].astype(int))
    return max(list(df_project_distribution_value['Project Value']))


def update_project_value_overview_fig(df, slider_value):
    df_project_distribution_value = clean_data(df)

    df_project_distribution_value = df_project_distribution_value[
        (df_project_distribution_value['Project Value'] >= slider_value[0]) &
        (df_project_distribution_value['Project Value'] <= slider_value[1])]

    return generate_bar_graph(df_project_distribution_value)


