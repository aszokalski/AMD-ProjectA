from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import pandas as pd
import json
app = FastAPI()


@app.get("/generate_dataset")
async def generate_dataset():
    df = pd.read_csv("data/dataset_long_name_ORIGINAL.csv")
    return {
        "data": json.loads(df.to_json(orient="records"))
    }

@app.get("/generate_tab_file")
async def generate_dataset():
    df = pd.read_csv("data/dataset_long_name_ORIGINAL.csv")
    columns = df.columns.tolist()
    types = ['discrete' for _ in columns]

    with open("data/dataset_long_name_orange.tab", 'w') as file:
        file.write('\t'.join(columns) + '\n')
        file.write('\t'.join(types) + '\n')
        file.write('class' + '\n')

        for index, row in df.iterrows():
            if row.values[0].startswith('-'):
                break
            file.write('\t'.join(map(str, row.values)) + '\n')

    return FileResponse(Path("data/dataset_long_name_orange.tab"))
