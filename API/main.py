from io import BytesIO
from typing import Union
import pandas as pd
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from PredicitonModel import Model
from DataModel import DataModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"API": "Proyecto 1 - Etapa 2"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Se sube el archivo de Excel sin etiquetar desde el front
@app.post("/predict")
def make_predictions(file: UploadFile):
    try:
        # Leer el archivo CSV en un DataFrame
        content = await file.read()
        df = pd.read_csv(BytesIO(content))

        # Hacer algo con el DataFrame, por ejemplo, imprimir las primeras filas
        print(df.head())

        # Puedes realizar cualquier operación que necesites con el DataFrame aquí

        return JSONResponse(content={"message": "Archivo CSV cargado exitosamente"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


    #df.columns = dataModel.columns()
    #prediction_model = Model()
    #result = prediction_model.make_predictions(df.columns)
    #return result
