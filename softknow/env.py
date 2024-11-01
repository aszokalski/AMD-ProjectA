import os
MEDKNOW_API_HOST = os.getenv("MEDKNOW_API_HOST", "localhost")
MEDKNOW_API_PORT = os.getenv("MEDKNOW_API_PORT", "8000")
MEDKNOW_API_URL = f"http://{MEDKNOW_API_HOST}:{MEDKNOW_API_PORT}"

MLFLOW_HOST = os.getenv("MLFLOW_HOST", "localhost")
MLFLOW_PORT = os.getenv("MLFLOW_PORT", "5000")
MLFLOW_URI = f"http://{MLFLOW_HOST}:{MLFLOW_PORT}"

MODEL_REPOSITORY = os.getenv("MODEL_REPOSITORY", "/model_repository")