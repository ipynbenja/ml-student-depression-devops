from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from typing import Annotated
from starlette.background import BackgroundTask

import pandas as pd
import tempfile
import os
import io
import zipfile

from src.model_utils import (
    predecir_estudiante, 
    predecir_dataframe,
    obtener_importancia_caso
)

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


@app.post("/case-importance")
def importancia_caso(student: StudentRequest):
    """
    Obtiene las variables que más influyeron en la
    predicción de un estudiante específico.
    """

    try:
        resultado = obtener_importancia_caso(student)

        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=(
                "Error al obtener la importancia "
                f"del caso: {str(e)}"
            )
        )


@app.post("/predict-file")
async def predict_file(
    file: Annotated[UploadFile, File(...)]
):
    """
    Procesa un archivo CSV o XLSX y devuelve las predicciones.
    Retorna 400 si el archivo está vacío, tiene un formato inválido
    o no contiene las columnas requeridas por el modelo.
    """

    output_path = None

    try:
        # Validar la extensión del archivo.
        extension = os.path.splitext(file.filename or "")[1].lower()

        if extension not in {".csv", ".xlsx"}:
            raise HTTPException(
                status_code=400,
                detail="Solo se permiten archivos CSV o XLSX."
            )

        # Leer el contenido del archivo.
        contenido = await file.read()

        if not contenido or not contenido.strip():
            raise HTTPException(
                status_code=400,
                detail="El archivo está vacío."
            )

        # Leer el CSV o XLSX desde memoria.
        try:
            buffer = io.BytesIO(contenido)

            if extension == ".csv":
                df = pd.read_csv(buffer)
            else:
                df = pd.read_excel(buffer)

        except (
            pd.errors.EmptyDataError,
            pd.errors.ParserError,
            UnicodeDecodeError,
            ValueError,
            zipfile.BadZipFile,
        ) as exc:
            raise HTTPException(
                status_code=400,
                detail="El archivo está vacío o tiene un formato inválido."
            ) from exc

        # Validar que existan registros y columnas.
        if df.empty or len(df.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="El archivo no contiene registros para procesar."
            )

        # Validar las columnas requeridas por el modelo.
        columnas_requeridas = {
            "Sleep Duration",
            "Have you ever had suicidal thoughts ?",
            "Work/Study Hours",
            "Study Satisfaction",
            "Degree",
            "Financial Stress",
            "Academic Pressure",
            "Gender",
            "CGPA",
            "Age",
            "Dietary Habits",
            "Family History of Mental Illness",
        }

        columnas_faltantes = columnas_requeridas - set(df.columns)

        if columnas_faltantes:
            raise HTTPException(
                status_code=400,
                detail={
                    "mensaje": (
                        "El archivo no contiene todas las "
                        "columnas requeridas por el modelo."
                    ),
                    "columnas_faltantes": sorted(columnas_faltantes),
                },
            )

        # Ejecutar las predicciones.
        try:
            resultado = predecir_dataframe(df)

        except (ValueError, KeyError) as exc:
            raise HTTPException(
                status_code=400,
                detail=(
                    "No se pudo procesar el archivo. "
                    "Verifica los tipos y valores de los datos."
                ),
            ) from exc

        # Crear el archivo temporal de salida.
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:
            output_path = temp_file.name

        # Guardar las predicciones.
        if extension == ".csv":
            resultado.to_csv(output_path, index=False)
        else:
            resultado.to_excel(output_path, index=False)

        # Devolver el archivo y eliminarlo tras enviarlo.
        return FileResponse(
            path=output_path,
            filename=f"predictions{extension}",
            media_type="application/octet-stream",
            background=BackgroundTask(os.unlink, output_path),
        )

    except HTTPException:
        raise

    except Exception as exc:
        # Registrar el error real en los logs del servidor.
        print(f"Error inesperado en /predict-file: {exc!r}")

        raise HTTPException(
            status_code=500,
            detail="Error interno al procesar el archivo.",
        ) from exc

    finally:
        await file.close()