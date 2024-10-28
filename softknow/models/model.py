from abc import ABC
from pandas import DataFrame
from dataclasses import dataclass


@dataclass
class EvaluationResult:
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
