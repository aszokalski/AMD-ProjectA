import logging

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
from model.model import Model, EvaluationResult
import pandas as pd
import mlflow
import matplotlib.pyplot as plt
import numpy as np
from utils.env import MLFLOW_URI
from utils.mlflow_utils import get_latest_model_uri

mlflow.set_tracking_uri(MLFLOW_URI)
logger = logging.getLogger(__name__)


class OneR(Model):
    @classmethod
    def train_impl(cls, name: str, dataframe: pd.DataFrame, target_column: str):
        X = dataframe.drop(columns=[target_column])
        y = dataframe[target_column]

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

        def predict(model_input):
            return model_input[best_feature].map(best_rule)

        mlflow.pyfunc.log_model("model", python_model=predict, pip_requirements=["pandas"])

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