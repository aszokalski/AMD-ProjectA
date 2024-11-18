from typing import Dict, Tuple
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess(
        df: pd.DataFrame,
        target_column: str | None = None,
        label_encoders: Dict[str, LabelEncoder] | None = None
) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder] | None]:
    df_encoded = df.copy()

    if target_column is not None:
        df_encoded = df_encoded.dropna(subset=[target_column])
    df_encoded = df_encoded.fillna("Unknown")

    if label_encoders is None:
        label_encoders = {}

        for column in df.columns:
            if df[column].dtype == 'object' or df[column].dtype.name == 'category':
                encoder = LabelEncoder()
                df_encoded[column] = encoder.fit_transform(df_encoded[column])
                label_encoders[column] = encoder

        return df_encoded, label_encoders
    else:
        for column in df.columns:
            if column in label_encoders:
                df_encoded[column] = label_encoders[column].transform(df_encoded[column])

        return df_encoded, None
