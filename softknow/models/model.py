from abc import ABC
from pandas import DataFrame
from dataclasses import dataclass
from ..deployment import deploy_model
import mlflow

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
    def deploy(cls, version: int):
        deploy_model(cls.__name__, str(version))


