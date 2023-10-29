from typing import Union
import pandas as pd
from fastapi import FastAPI
from joblib import load

from API.PredicitonModel import Model
from DataModel import DataModel
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"API": "Proyecto 1 - Etapa 2"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Se sube el archivo de Excel sin etiquetar desde el front
@app.post("/predict")
def make_predictions(dataModel: DataModel):
    # Se convierte el Excel en un DataFrame:
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    prediction_model = Model()
    result = prediction_model.make_predictions(df.columns)
    return result
