from fastapi import FastAPI
from logging import getLogger

app = FastAPI()
logger = getLogger(__name__)


# @app.on_event("startup")
# async def startup_event():
#     logger.info("Initializing resources...")


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/generate_dataset")
def generate_dataset():
    return "[]"