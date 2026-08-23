from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi.responses import FileResponse

import pandas as pd
import tempfile
import os

from src.model_utils import predecir_estudiante, predecir_dataframe

from Request.StudentRequest import StudentRequest


app = FastAPI(
    title="Student Depression Prediction API",
    description="API para predicción de depresión estudiantil utilizando Random Forest",
    version="1.0.0"
)


@app.get("/")
def root():
    """
    Endpoint principal.
    """

    return {
        "message": "Student Depression Prediction API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/predict")
def predict(student: StudentRequest):
    """
    Realiza una predicción individual.
    """

    return predecir_estudiante(student)


@app.post("/predict-file")
async def predict_file(
    file: UploadFile = File(...)
):
    """
    Realiza predicciones sobre un
    archivo CSV o XLSX y retorna
    el resultado al usuario.
    """

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in [
        ".csv",
        ".xlsx"
    ]:
        return {
            "error":
            "Solo se permiten archivos CSV o XLSX"
        }

    if extension == ".csv":
        df = pd.read_csv(file.file)
    else:
        df = pd.read_excel(file.file)

    resultado = predecir_dataframe(df)

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    )

    output_path = temp_file.name

    if extension == ".csv":
        resultado.to_csv(
            output_path,
            index=False
        )
    else:
        resultado.to_excel(
            output_path,
            index=False
        )

    return FileResponse(
        path=output_path,
        filename=f"predictions{extension}",
        media_type="application/octet-stream"
    )