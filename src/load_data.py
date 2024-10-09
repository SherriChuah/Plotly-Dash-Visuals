from assets.config import Config
import pandas as pd

config = Config()


def preprocess_data(path: str):
    df_raw = pd.read_excel(path, header=[0, 1, 2])

    df_raw[
        ("Fast Followers member", "Unnamed: 0_level_1", "Organisations")] = (
        df_raw[
            ("Fast Followers member", "Unnamed: 0_level_1", "Organisations")
        ].ffill())

    df_raw = df_raw[~(df_raw[(
                "Fast Followers member", "Unnamed: 1_level_1", "Project Name")
            ]
            .str.lower()
            .str.contains("total", na=True))]

    return df_raw


def distinguish_data(tab, cleaned_data, council: str = config.default_council):
    if tab == "overview":
        return cleaned_data
    elif tab == "council_view":
        return cleaned_data[cleaned_data['Organisations'] == council]


def get_project_classification(df):
    df = df.droplevel(level=[0, 1], axis=1)

    column_index = df.columns.get_loc('Solar')

    df = df.iloc[:, column_index:]
    return list(df.columns)
