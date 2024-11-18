import os
import pickle
import tempfile
import mlflow
import pandas as pd
from pandas import DataFrame
from dataclasses import dataclass
from abc import ABC

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
    def train(cls, dataset: DataFrame, client: str, target_column: str) -> EvaluationResult:
        name = f"{client}.{cls.__name__}"
        mlflow.set_experiment(name)
        mlflow.autolog()

        dataset, encoders = preprocess(dataset)
        encoders_bytes = pickle.dumps(encoders)

        with mlflow.start_run():
            # Save encoders to a temporary file and log it
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, "label_encoders.pkl")
                with open(temp_file_path, "wb") as f:
                    f.write(encoders_bytes)

                mlflow.log_artifact(temp_file_path, artifact_path="preprocessors")

                # Clean up the temporary file
                os.remove(temp_file_path)

            return cls.train_impl(name, dataset, target_column)

    @classmethod
    def train_impl(cls, name: str, dataset: DataFrame, target_column: str) -> EvaluationResult:
        pass

    @classmethod
    def predict(cls, data: dict, client: str):
        model_uri = get_latest_model_uri(f"{client}.{cls.__name__}")
        model = mlflow.pyfunc.load_model(model_uri)

        parts = model_uri.split("/")
        model_name = parts[1]
        model_version = parts[2]

        client = mlflow.MlflowClient()
        model_version_details = client.get_model_version(name=model_name, version=model_version)
        run_id = model_version_details.run_id

        artifact_path = "preprocessors/label_encoders.pkl"

        encoders_path = mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path=artifact_path)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(open(encoders_path, "rb").read())
            temp_file_path = temp_file.name

        with open(temp_file_path, "rb") as f:
            encoders = pickle.load(f)

        os.remove(temp_file_path)

        data = pd.DataFrame(data, index=[0])
        preprocessed, _ = preprocess(data, encoders)

        return model.predict(preprocessed)