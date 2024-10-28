from fastapi import FastAPI
from logging import getLogger
from env import MEDKNOW_API_URL, MLFLOW_URI
from preprocessing import preprocess
from models.id3 import ID3
import pandas as pd
import mlflow
import requests
import asyncio

mlflow.set_tracking_uri(MLFLOW_URI)

app = FastAPI()
logger = getLogger(__name__)

models = [
    ID3
]


@app.on_event("startup")
async def startup_event():
    while True:
        try:
            train_model()
            break
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to Medknow API. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"An error occurred: {e}. Trying again in 5 seconds...")
            await asyncio.sleep(5)


@app.get("/train_model")
def train_model():
    logger.info("Training models...")
    dataset = requests.get(f"{MEDKNOW_API_URL}/generate_dataset")
    dataframe = pd.read_json(dataset.json())

    dataframe = preprocess(dataframe)

    results = {
        model.__name__: model.train(dataframe) for model in models
    }

    return results


@app.post("/deploy_model/{model_name}/{model_version}")
def deploy_model(model_name: str, model_version: int):
    logger.info(f"Deploying model {model_name} version {model_version}")
    model = next(model for model in models if model.__name__ == model_name)
    model.deploy(model_version)

    return {"message": "Model deployed successfully"}