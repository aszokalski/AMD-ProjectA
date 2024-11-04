import pandas as pd


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df['astigmatic'] = df['astigmatic'].astype(int)
    return df
