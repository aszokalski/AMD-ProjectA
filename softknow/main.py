from typing import Literal

from fastapi import FastAPI
from logging import getLogger
from utils.env import MEDKNOW_API_URL, MLFLOW_URI, FUNGIDATA_API_URL
from data_manipulation.preprocessing import preprocess
from model.id3 import ID3
from model.oner import OneR
import pandas as pd
import mlflow
import requests

mlflow.set_tracking_uri(MLFLOW_URI)

app = FastAPI()
logger = getLogger(__name__)

models = [
    ID3,
    OneR
]


@app.get("/train_model/{client}")
def train_model(client: Literal["medknow", "fungidata"]):
    logger.info("Training models...")

    response = requests.get(f"{
        MEDKNOW_API_URL if client == 'medknow' else FUNGIDATA_API_URL
        }/generate_dataset").json()
    dataframe = pd.DataFrame(response["data"])
    target_column = response["target"]

    results = {
        model.__name__: model.train(dataframe, client, target_column) for model in models
    }

    return results


@app.post("/predict/{client}/{model_name}")
def predict(client: Literal["medknow", "fungidata"], model_name: str, data: dict):
    model = next(filter(lambda m: m.__name__ == model_name, models))
    res = model.predict(data, client)
    return {
        "prediction": res.tolist()[0]
    }
