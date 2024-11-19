import logging
import tempfile
from typing import Dict

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, \
    ConfusionMatrixDisplay
from model.model import Model, EvaluationResult
import pandas as pd
import mlflow
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder
from utils.env import MLFLOW_URI

mlflow.set_tracking_uri(MLFLOW_URI)
logger = logging.getLogger(__name__)


class OneR(Model):
    @classmethod
    def train_impl(cls, name: str, dataframe: pd.DataFrame, target_column: str,
                   encoders: Dict[str, LabelEncoder]) -> EvaluationResult:
        X = dataframe.drop(columns=[target_column])
        y = dataframe[target_column]

        best_feature = None
        best_rule = None
        lowest_error_rate = float("inf")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        for feature in X_train.columns:
            rules = {}
            for value in set(X_train[feature]):
                mode_class = y_train[X_train[feature] == value].mode()[0]
                rules[value] = mode_class

            predictions = X_train[feature].map(rules)
            error_rate = (predictions != y_train).mean()

            if error_rate < lowest_error_rate:
                best_feature = feature
                best_rule = rules
                lowest_error_rate = error_rate

        instance = cls()
        instance.rule = best_rule
        instance.target_column = best_feature

        def predict(model_input):
            return model_input[best_feature].map(best_rule).fillna(default_class)


        default_class = y_train.mode()[0]
        mlflow.pyfunc.log_model("model", python_model=predict, pip_requirements=["pandas"])

        y_pred = X_test[best_feature].map(best_rule).fillna(default_class)

        errors_list = (y_pred != y_test)
        errors = {}
        rules_val_count = {}
        for rule, value in best_rule.items():
            errors[rule] = 0
            rules_val_count[rule] = 0
        x_test_feature = list(X_test[best_feature])
        i = 0
        for er in errors_list:
            if er is True:
                errors[x_test_feature[i]] += 1
            rules_val_count[x_test_feature[i]] += 1
            i += 1

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        cm = confusion_matrix(y_test, y_pred, labels=np.unique(y))
        fig, ax = plt.subplots(figsize=(18, 8))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y))
        disp.plot(ax=ax)

        mlflow.log_figure(fig, "confusion_matrix.png")
        plt.close(fig)

        mlflow.log_param("best_feature", best_feature)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_dict(best_rule, "rule.json")
        mv = mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", name)
        output = ""

        encoder_feature = encoders.get(best_feature)
        encoder_class = encoders.get(target_column)

        if encoder_feature is None or encoder_class is None:
            logger.error("Encoder for best_feature or target_column not found.")
            raise ValueError("Missing encoders for required columns.")

        for rule, value in best_rule.items():
            try:
                decoded_rule = encoder_feature.inverse_transform([rule])[0]
            except ValueError as e:
                logger.warning(f"Unseen rule value '{rule}' for feature '{best_feature}'. Assigning 'Unknown'.")
                decoded_rule = "Unknown"

            try:
                decoded_value = encoder_class.inverse_transform([value])[0]
            except ValueError as e:
                logger.warning(
                    f"Unseen target value '{value}' for target column '{target_column}'. Assigning 'Unknown'.")
                decoded_value = "Unknown"

            output += f"({best_feature}, {decoded_rule}, {decoded_value}) : ({errors[rule]}, {rules_val_count[rule]})\n"

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = f"{temp_dir}/oneR_OUTPUT.txt"
            with open(filename, "w") as f:
                f.write(output)
            mlflow.log_artifact(filename)

        return EvaluationResult(
            version=mv.version,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1=f1
        )