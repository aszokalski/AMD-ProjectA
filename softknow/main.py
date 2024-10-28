from fastapi import FastAPI
from logging import getLogger
from env import MEDKNOW_API_URL, MLFLOW_URI
from preprocessing import preprocess
from id3 import ID3
import pandas as pd
import mlflow
import requests

mlflow.set_tracking_uri(MLFLOW_URI)

app = FastAPI()
logger = getLogger(__name__)

models = [
    ID3
]


# @app.on_event("startup")
# async def startup_event():
#     while True:
#         try:
#             train_model()
#             deploy_model("ID3", 1)
#             break
#         except requests.exceptions.ConnectionError:
#             logger.error("Failed to connect to Medknow API. Retrying in 5 seconds...")
#             await asyncio.sleep(5)


@app.get("/train_model")
def train_model():
    logger.info("Training models...")
    dataset = requests.get(f"{MEDKNOW_API_URL}/generate_dataset")
    dataframe = pd.DataFrame(dataset.json()["data"])

    dataframe = preprocess(dataframe)

    results = {
        model.__name__: model.train(dataframe) for model in models
    }

    return results


@app.post("/predict/{model_name}/{model_version}")
def predict(model_name: str, model_version: int, data: dict):
    logger.info(f"Predicting using {model_name} version {model_version}...")
    model = next(filter(lambda m: m.__name__ == model_name, models))
    return model.predict(model_version, data)
