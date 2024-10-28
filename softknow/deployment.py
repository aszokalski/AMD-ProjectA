import os
import shutil
import mlflow
from mlflow.tracking import MlflowClient
import yaml
import logging
from env import MLFLOW_URI, MODEL_REPOSITORY

# mlflow.set_tracking_uri(MLFLOW_URI)
client = MlflowClient()
logger = logging.getLogger(__name__)

def download_model(model_name, model_version):
    model_uri = f"models:/{model_name}/{model_version}"
    local_path = mlflow.pyfunc.download_model(model_uri=model_uri)
    return local_path


def determine_implementation(model_path):
    if os.path.exists(os.path.join(model_path, "model.pkl")):
        return "sklearn", "model.pkl"
    elif os.path.exists(os.path.join(model_path, "model.pt")):
        return "pytorch", "model.pt"
    elif os.path.exists(os.path.join(model_path, "model.h5")):
        return "tensorflow", "model.h5"
    else:
        return "mlflow.pyfunc", "model.pkl"


def create_model_config(model_name, implementation, model_file):
    config = {
        "name": model_name,
        "implementation": implementation,
        "parameters": {
            "model_path": model_file
        }
    }
    return config


def deploy_model(model_name: str, model_version: str):
    client.transition_model_version_stage(
        name=model_name,
        version=model_version,
        stage="Production"
    )

    logger.info(f"Deploying {model_name} version {model_version} to MLServer.")
    model_path = download_model(model_name, model_version)

    implementation, model_file = determine_implementation(model_path)

    dest_dir = os.path.join(MODEL_REPOSITORY, model_name)

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir, exist_ok=True)

    for item in os.listdir(model_path):
        s = os.path.join(model_path, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    config = create_model_config(model_name, implementation, model_file)
    with open(os.path.join(dest_dir, "model.yml"), "w") as f:
        yaml.dump(config, f)

    logger.info(f"Model {model_name} version {model_version} deployed successfully.")