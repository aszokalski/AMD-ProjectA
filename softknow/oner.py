import logging

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
from model import Model, EvaluationResult
import pandas as pd
import mlflow
import matplotlib.pyplot as plt
import numpy as np
from env import MLFLOW_URI
from mlflow_utils import get_latest_model_uri, deploy_model_to_production

mlflow.set_tracking_uri(MLFLOW_URI)
logger = logging.getLogger(__name__)


class OneR(Model):
    def __init__(self):
        self.rule = None
        self.target_column = None

    @classmethod
    def train_impl(cls, name: str, dataframe: pd.DataFrame):
        mlflow.set_experiment(name)

        with mlflow.start_run():

            X = dataframe.drop(columns=["lens_type"])
            y = dataframe["lens_type"]

            best_feature = None
            best_rule = None
            lowest_error_rate = float("inf")

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

            for feature in X_train.columns:
                rules = {}
                for value in set(X_train[feature]):
                    mode_class = y_train[X_train[feature] == value].mode()[0]
                    rules[value] = mode_class

                predictions = X_train[feature].map(rules)
                print(predictions)
                error_rate = (predictions != y_train).mean()
                print(error_rate)

                if error_rate < lowest_error_rate:
                    best_feature = feature
                    best_rule = rules
                    lowest_error_rate = error_rate

            instance = cls()
            instance.rule = best_rule
            instance.target_column = best_feature

            y_pred = X_test[best_feature].map(best_rule)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')

            cm = confusion_matrix(y_test, y_pred, labels=np.unique(y))
            fig, ax = plt.subplots(figsize=(18, 8))
            disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                          display_labels=np.unique(y))
            disp.plot(ax=ax)

            mlflow.log_figure(fig, "confusion_matrix.png")
            plt.close(fig)

            mlflow.log_param("best_feature", best_feature)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_dict(best_rule, "rule.json")
            mv = mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", name)

        return EvaluationResult(
            version=mv.version,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1=f1
        )

    @classmethod
    def deploy(cls, version: int):
        deploy_model_to_production(cls.__name__, str(version))

    @classmethod
    def predict(cls, data: dict):
        model_uri = get_latest_model_uri(cls.__name__)
        model = mlflow.pyfunc.load_model(model_uri)

        best_feature = model.metadata.params["best_feature"]
        rule = model.metadata.artifacts["rule.json"]

        data = pd.DataFrame(data, index=[0])
        y_pred = data[best_feature].map(rule)
        return y_pred
