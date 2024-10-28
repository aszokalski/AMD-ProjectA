import asyncio

from fastapi import FastAPI
from logging import getLogger
from env import MEDKNOW_API_URL
from models.id3 import ID3
import pandas as pd

import requests

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

    results = {
        model.__name__: model.train(dataframe) for model in models
    }

    return results
