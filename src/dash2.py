import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from src.load_data import distinguish_data


def generate_project_classification_visualizations(df: pd.DataFrame, tab: str):
    df_clean = clean_data(df.copy())
    df_data = distinguish_data(tab, df_clean)
    df_data = df_data[df_data['Count'] != 0]

    df_data = df_data.sort_values(['Count'], ascending=True)

    if tab == "overview":
        fig_bar_chart = generate_bar_fig(
            df_data,
            "Count",
            "Organisations",
            "Project Classification Breakdown",
            "Project Classification Count Per Council"
        )
        donut_fig = None

    else:
        fig_bar_chart = generate_bar_fig(
            df_data,
            "Project Classification",
            "Count",
            "Project Classification Breakdown",
            "Project Classification Distribution"
        )
        donut_fig = generate_donut_fig(df_data.copy())

    return fig_bar_chart, donut_fig


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw data and structure it for visualisation
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    # Get specific columns related to project classification
    column_index = df.columns.get_loc(
        ('Project Classification', 'Power Generation', 'Solar'))

    df_project_classification = df.iloc[:, column_index:]

    # Organisation and project name cols
    df_organisation_project_name = df.iloc[:, :2]

    # Concat above together
    df_project_classification = pd.concat(
        [df_organisation_project_name, df_project_classification], axis=1)

    df_project_classification.columns = (
        df_project_classification.columns.droplevel(0))

    # Fill with 0 if nan
    columns_to_fill = [('Power Generation', 'Solar'),
                       ('Power Generation', 'Wind'),
                       ('Power Generation', 'Hydrogen'),
                       ('Heat generation', 'Heat networks'),
                       ('Heat generation', 'Heat pumps'),
                       ('Storage', 'Battery'),
                       ('Storage', 'Thermal'),
                       ('Buildings', 'Retrofit'),
                       ('Transport', 'Electric vehicles'),
                       ('Horticulture', 'Farming'),
                       ('Horticulture', 'Multi-'),
                       ('Horticulture', 'Comments (types)')]

    df_project_classification[columns_to_fill] = df_project_classification[
        columns_to_fill].fillna(0)

    # Deal with classifications that are not int
    for col in columns_to_fill:
        df_project_classification[col] = df_project_classification[col].apply(
            lambda x: 0 if isinstance(x, str) else int(x)
        )

    # Group by Organisation to get count
    df_project_classification_groupby_organisation = (
        df_project_classification.groupby(
            ('Unnamed: 0_level_1', 'Organisations'))[
            columns_to_fill
        ].sum()).reset_index()

    # Melt dataframe
    df_melted = df_project_classification_groupby_organisation.melt(
        id_vars=[('Unnamed: 0_level_1', 'Organisations')],
        value_vars=columns_to_fill)

    # Rename columns
    df_melted.columns = ['Organisations', 'Project Classification',
                         'Project Classification Breakdown', 'Count']

    # Get Project Classification higher level count
    df_melted['Project Classification Count'] = (
        df_melted.groupby(['Organisations', 'Project Classification'])[
                            'Count'].transform('sum'))

    return df_melted


def generate_bar_fig(df: pd.DataFrame, x, y, color, title):
    max_value = len(set(df[y]))
    fig_height = max(700, max_value * 40)

    fig_bar_chart = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        height=fig_height)

    fig_bar_chart.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=1.1,
        xanchor="right",
        x=1))

    return fig_bar_chart


def generate_donut_fig(df: pd.DataFrame):
    temp = df[['Project Classification', 'Organisations',
              'Project Classification Count']].drop_duplicates()

    label = list(temp['Project Classification']) + list(
        df['Project Classification Breakdown'])

    count_organisation = len(list(temp['Organisations']))
    list_organisation = [''] * count_organisation

    parents = list_organisation + list(df['Project Classification'])

    values = list(temp['Project Classification Count']) + list(df['Count'])

    fig = go.Figure(go.Sunburst(
        labels=label,
        parents=parents,
        values=values,
        branchvalues="total",
    ))

    fig.update_layout(
        height=550,  # Adjust height as needed
        width=550,  # Adjust width as needed
    )

    return fig


def update_dash2_visuals_func(df, council):
    df_cleaned = clean_data(df)
    df_council_and_projects = distinguish_data('council_view', df_cleaned, council)
    df_council_and_projects = df_council_and_projects.drop_duplicates()

    df_council_and_projects = df_council_and_projects.sort_values(['Count'], ascending=True)

    fig_bar_chart = generate_bar_fig(
        df_council_and_projects,
        "Project Classification",
        "Count",
        "Project Classification Breakdown",
        "Project Classification Distribution"
    )

    donut_fig = generate_donut_fig(df_council_and_projects)

    return fig_bar_chart, donut_fig


def update_project_classification_overview_fig(df, select_some, select_all):
    df_clean = clean_data(df.copy())

    if select_all != ['All']:
        df_clean = df_clean[df_clean[
            'Project Classification Breakdown'].isin(select_some)].copy()
        df_clean = df_clean[df_clean['Count'] != 0]

    fig_bar_chart = generate_bar_fig(
        df_clean,
        "Count",
        "Organisations",
        "Project Classification Breakdown",
        "Project Classification Count Per Council"
    )
    return fig_bar_chart
