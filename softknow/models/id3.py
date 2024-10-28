from .model import Model, EvaluationResult
from pandas import DataFrame


class ID3(Model):
    @classmethod
    def train_impl(cls, name: str, dataframe: DataFrame):
        return EvaluationResult(accuracy=0.0, precision=0.0, recall=0.0, f1=0.0)
