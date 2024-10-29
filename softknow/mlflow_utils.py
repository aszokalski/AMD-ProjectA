import mlflow


def get_latest_model_uri(model_name: str) -> str:
    client = mlflow.tracking.MlflowClient()
    latest_version_info = client.get_latest_versions(model_name, stages=["Production"])
    if not latest_version_info:
        raise ValueError("No production model found for the specified model name.")
    latest_version = latest_version_info[0]
    return f"models:/{model_name}/{latest_version.version}"


def deploy_model_to_production(model_name: str, model_version: str) -> str:
    client = mlflow.tracking.MlflowClient()
    client.transition_model_version_stage(
        name=model_name,
        version=model_version,
        stage="Production"
    )