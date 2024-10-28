from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, \
    ConfusionMatrixDisplay
from .model import Model, EvaluationResult
from pandas import DataFrame
from sklearn import tree
import mlflow
import matplotlib.pyplot as plt


class ID3(Model):
    @classmethod
    def train_impl(cls, name: str, dataframe: DataFrame):
        mlflow.set_experiment(name)
        mlflow.autolog()

        X = dataframe.drop(["target"], axis=1)
        y = dataframe["target"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        clf = tree.DecisionTreeClassifier(criterion="entropy")

        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)
        fig, ax = plt.subplots(figsize=(18, 8))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                      display_labels=clf.classes_)
        disp.plot()

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
