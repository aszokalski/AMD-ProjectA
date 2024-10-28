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
    def predict(cls, version: int, data: dict):
        """
        Make predictions using a specific version of the ID3 model.

        Parameters:
        - version (int): The version number of the model to use for prediction.
        - data (dict): The input data for prediction.

        Returns:
        - dict: A dictionary containing the predictions.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Loading model version {version} for prediction.")

        try:
            # Construct the model URI
            model_uri = f"models:/{cls.__name__}/{version}"

            # Load the model using MLflow
            # Using a temporary directory to load the model
            model = mlflow.pyfunc.load_model(model_uri=model_uri)
            logger.info(f"Model version {version} loaded successfully.")
        except mlflow.exceptions.MlflowException as e:
            logger.error(f"Failed to load model version {version}: {e}")
            return {"error": f"Failed to load model version {version}."}
        except Exception as e:
            logger.error(f"Unexpected error while loading model: {e}")
            return {"error": "An unexpected error occurred while loading the model."}

        try:
            # Convert input data dict to DataFrame
            # Assuming data is a dictionary where keys are feature names and values are feature values
            input_df = pd.DataFrame([data])
            logger.debug(f"Input DataFrame: {input_df}")

            # Make predictions
            predictions = model.predict(input_df)
            logger.info(f"Predictions made successfully: {predictions}")

            # If predictions are in a NumPy array or Pandas Series, convert them to list
            if isinstance(predictions, (pd.Series, pd.DataFrame)):
                predictions = predictions.tolist()
            elif isinstance(predictions, (np.ndarray)):
                predictions = predictions.tolist()

            return {"predictions": predictions}
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return {"error": "An error occurred during prediction."}