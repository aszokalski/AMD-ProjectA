import logging

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
from model import Model, EvaluationResult
import pandas as pd
from sklearn import tree
import mlflow
import matplotlib.pyplot as plt
import numpy as np
from env import MLFLOW_URI
from mlflow_utils import get_latest_model_uri, deploy_model_to_production

mlflow.set_tracking_uri(MLFLOW_URI)

class ID3(Model):
    @classmethod
    def train_impl(cls, name: str, dataframe: pd.DataFrame):
        mlflow.set_experiment(name)
        mlflow.autolog()

        X = dataframe.drop(["lens_type"], axis=1)
        y = dataframe["lens_type"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        clf = tree.DecisionTreeClassifier(criterion="entropy")

        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)

        # Metrics with 'macro' or 'weighted' averaging for multiclass targets
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)
        fig, ax = plt.subplots(figsize=(18, 8))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                      display_labels=clf.classes_)
        disp.plot(ax=ax)

        mlflow.log_figure(fig, "confusion_matrix.png")
        plt.close(fig)

        mv = mlflow.register_model(
            f"runs:/{mlflow.active_run().info.run_id}/model",
            name
        )

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
        model = mlflow.xgboost.load_model(model_uri)

        data = {key: [np.float64(value)] for key, value in data.items()}

        return model.predict(data)
