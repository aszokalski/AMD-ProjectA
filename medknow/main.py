from fastapi import FastAPI
from logging import getLogger

app = FastAPI()
logger = getLogger(__name__)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/generate_dataset")
def generate_dataset():
    return "[]"
