from fastapi import FastAPI
import pandas as pd
import json
app = FastAPI()


@app.get("/generate_dataset")
async def generate_dataset():
    df = pd.read_csv("data/dataset_long_name_ORIGINAL.csv")
    return {
        "data": json.loads(df.to_json(orient="records"))
    }
