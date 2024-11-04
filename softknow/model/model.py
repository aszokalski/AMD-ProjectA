from abc import ABC

import mlflow
import pandas as pd
from pandas import DataFrame
from dataclasses import dataclass

from utils.mlflow_utils import get_latest_model_uri
from data_manipulation.preprocessing import preprocess


@dataclass
class EvaluationResult:
    version: int
    accuracy: float
    precision: float
    recall: float
    f1: float


class Model(ABC):
    @classmethod
    def train(cls, dataset: DataFrame) -> EvaluationResult:
        return cls.train_impl(cls.__name__, dataset)

    @classmethod
    def train_impl(cls, name: str, dataset: DataFrame) -> EvaluationResult:
        pass

    @classmethod
    def predict(cls, data: dict):
        model_uri = get_latest_model_uri(cls.__name__)
        model = mlflow.pyfunc.load_model(model_uri)

        data = pd.DataFrame(data, index=[0])

        preprocessed = preprocess(data)

        return model.predict(preprocessed)
