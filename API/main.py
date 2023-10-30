import io
import os
from io import StringIO, BytesIO
from tempfile import NamedTemporaryFile
from typing import Union
from fastapi import FastAPI, File, UploadFile, Response, BackgroundTasks
import csv
import codecs
import pandas as pd
import joblib

from PredicitonModel import Model

app = FastAPI()


@app.get("/")
def read_root():
    return {"API": "Proyecto 1 - Etapa 2"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



def limpiar_contenido(contenido):
    # Reemplazar los caracteres de salto de línea por espacios en blanco
    contenido_limpio = contenido.replace('\r', ' ').replace('\n', '|')
    return contenido_limpio


@app.post("/predict")
async def upload_file(file: UploadFile):
    # Verificar si el archivo subido es un archivo CSV
    if not file.filename.endswith(".csv"):
        return {"error": "Solo se permiten archivos CSV"}

    # Leer el archivo CSV con codificación UTF-8
    contents = await file.read()

    # Limpiar el contenido
    contenido_limpio = limpiar_contenido(contents.decode('utf-8'))

    mi_dict = {}
    cont = 0
    arr = contenido_limpio.split('|')
    sdg = []
    for linea in arr:
        if linea:
            clave = arr[0].split(';')[0]
            if cont == 0:
                pass
            else:
                valor = linea
                sdg.append(valor)
                mi_dict[clave] = sdg
            cont += 1

    # Crear un DataFrame a partir del contenido limpio
    df_predict = pd.DataFrame(mi_dict)
    df_predict.columns = ['Textos_espanol']

    print(df_predict.shape[0])

    filename_model = "assets/tfidf_model.joblib"
    filename_transform = "assets/tfidf_transform.pkl"

    # Carga el modelo desde el archivo
    tfidf_model = joblib.load(filename_model)
    tfidf = joblib.load(filename_transform)

    df_prueba = pd.read_csv("./SinEtiquetatest_cat_345.csv", sep=';', encoding = 'utf8')
    df_prueba = df_prueba['Textos_espanol']

    # Prediccion:
    tfidf.transform(df_prueba)
    y_test_search_predict = tfidf_model.predict(df_prueba)

    print('res:', y_test_search_predict)

    df_prueba['sdg'] = y_test_search_predict[0:]

    # Convertir el DataFrame a JSON
    df_json = df_prueba.to_json()

    return df_json


@app.post("/upload-csv")
async def upload_csv(file: UploadFile):
    # Verificar que el archivo es un archivo CSV
    if not file.filename.endswith(".csv"):
        return {"error": "Solo se permiten archivos CSV"}

    # Leer el contenido del archivo
    contents = await file.read()

    try:
        # Leer el archivo CSV con Pandas
        df = pd.read_csv(pd.compat.StringIO(contents.decode('utf-8')))

        # Guardar el archivo CSV tal como se leyó
        df.to_csv("archivo_guardado.csv", index=False)

        return {"message": "Archivo CSV cargado y guardado exitosamente"}
    except Exception as e:
        return {"error": f"Error al procesar el archivo CSV: {str(e)}"}


