from fastapi import HTTPException
import os
from pathlib import Path

import joblib
import pandas as pd
import shap

from Request.StudentRequest import StudentRequest


# =============================================================================
# RUTAS DEL PROYECTO
# =============================================================================

#: Directorio raíz del proyecto.
#: Se calcula automáticamente tomando la carpeta padre de src.
ROOT_DIR = Path(__file__).resolve().parent.parent

#: Ruta absoluta del modelo Random Forest serializado.
MODEL_PATH = ROOT_DIR / "models" / "random_forest_model.pkl"

#: Ruta absoluta del pipeline de preprocesamiento serializado.
PREPROCESSOR_PATH = ROOT_DIR / "models" / "preprocessor.pkl"

#: Directorio donde se almacenan datasets y resultados.
DATA_PATH = ROOT_DIR / "data"


# =============================================================================
# CARGA DE RECURSOS
# =============================================================================

#: Modelo Random Forest cargado en memoria al iniciar la aplicación.
MODEL = joblib.load(MODEL_PATH)

#: Pipeline de preprocesamiento utilizado durante el entrenamiento.
PREPROCESSOR = joblib.load(PREPROCESSOR_PATH)

def predecir_estudiante(
    student: StudentRequest
) -> dict:
    """
    Realiza una predicción individual de depresión
    estudiantil utilizando el modelo entrenado.

    Parameters
    ----------
    student : StudentRequest
        Objeto que contiene todas las variables
        requeridas por el modelo para realizar
        la inferencia.

    Returns
    -------
    dict
        Diccionario con el resultado de la predicción.

        prediction : int
            Clase predicha por el modelo.

            - 0: No presenta depresión.
            - 1: Presenta depresión.

        probability_depression : float
            Probabilidad estimada de pertenecer
            a la clase positiva (depresión).
    """

    df = crear_dataframe_prediccion(student)

    X = transformar_dataset(df)

    prediction = int(
        MODEL.predict(X)[0]
    )

    probability = float(
        MODEL.predict_proba(X)[0][1]
    )

    return {
        "prediction": prediction,
        "probability_depression": round(
            probability,
            4
        )
    }

def predecir_dataframe(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Realiza predicciones sobre un DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset de entrada.

    Returns
    -------
    pd.DataFrame
        Dataset con predicción y probabilidad.
    """

    X = PREPROCESSOR.transform(df)

    X = pd.DataFrame(
        X,
        columns=PREPROCESSOR.get_feature_names_out()
    )

    prediction = MODEL.predict(X)

    probability = MODEL.predict_proba(X)[:, 1]

    resultado = df.copy()

    resultado["Prediction"] = prediction
    resultado["Probability_Depression"] = probability

    return resultado

def crear_dataframe_prediccion(
    student: StudentRequest
) -> pd.DataFrame:
    """
    Crea un DataFrame compatible con el pipeline
    de entrenamiento a partir de un StudentRequest.

    Parameters
    ----------
    student : StudentRequest
        Objeto que contiene todos los datos del
        estudiante requeridos para la predicción.

    Returns
    -------
    pd.DataFrame
        DataFrame listo para ser transformado por
        el preprocesador entrenado.
    """

    return pd.DataFrame([
        {
            "Gender": student.Gender,
            "Age": student.Age,
            "Academic Pressure": student.Academic_Pressure,
            "CGPA": student.CGPA,
            "Study Satisfaction": student.Study_Satisfaction,
            "Sleep Duration": student.Sleep_Duration,
            "Dietary Habits": student.Dietary_Habits,
            "Degree": student.Degree,
            "Have you ever had suicidal thoughts ?": (
                student.Suicidal_Thoughts
            ),
            "Work/Study Hours": student.Work_Study_Hours,
            "Financial Stress": student.Financial_Stress,
            "Family History of Mental Illness": (
                student.Family_History_Mental_Illness
            )
        }
    ])

def transformar_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica el pipeline de preprocesamiento utilizado
    durante el entrenamiento y retorna un DataFrame
    con los nombres de características esperados por
    el modelo.

    Esta función evita advertencias de scikit-learn
    relacionadas con la ausencia de nombres de columnas
    durante la etapa de inferencia.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset original sin transformar.

    Returns
    -------
    pd.DataFrame
        Dataset transformado mediante el
        preprocesador cargado desde disco.

        Las columnas corresponden a las
        características generadas por:

        - OneHotEncoder
        - BinaryEncoder
        - OrdinalEncoder
        - StandardScaler

        y conservan los nombres esperados
        por el modelo Random Forest.
    """

    X = PREPROCESSOR.transform(df)

    return pd.DataFrame(
        X,
        columns=PREPROCESSOR.get_feature_names_out()
    )

def guardar_resultados(
    df_resultado: pd.DataFrame,
    csv_original: str
) -> str:
    """
    Guarda un DataFrame con predicciones
    en formato CSV dentro del directorio
    configurado para almacenamiento.

    El nombre generado corresponde al nombre
    original del dataset agregando el sufijo
    '_predictions'.

    Parameters
    ----------
    df_resultado : pd.DataFrame
        Dataset que contiene las predicciones
        generadas por el modelo.

    csv_original : str
        Ruta del archivo utilizado como entrada.

    Returns
    -------
    str
        Ruta absoluta del archivo CSV generado.
    """

    nombre_archivo = os.path.basename(csv_original)

    output_name = nombre_archivo.replace(
        ".csv",
        "_predictions.csv"
    )

    output_path = DATA_PATH / output_name

    df_resultado.to_csv(
        output_path,
        index=False
    )

    return str(output_path)

def obtener_importancia_caso(
    student: StudentRequest
) -> dict:
    """
    Obtiene la importancia individual de las variables para
    una predicción específica utilizando SHAP.

    Parameters
    ----------
    student : StudentRequest
        Datos del estudiante utilizado para realizar
        la predicción.

    Returns
    -------
    dict
        Predicción, probabilidad y variables que más
        contribuyeron a la predicción.
    """

    # Crear DataFrame con los datos originales.
    df = crear_dataframe_prediccion(student)

    # Aplicar el mismo preprocesamiento utilizado durante
    # el entrenamiento.
    X = transformar_dataset(df)

    # Obtener el Random Forest desde el Pipeline.
    random_forest = MODEL.named_steps["model"]

    # Crear explicador SHAP para Random Forest.
    explainer = shap.TreeExplainer(random_forest)

    # Calcular valores SHAP.
    shap_values = explainer.shap_values(X)

    # Obtener la predicción.
    prediction = int(
        MODEL.predict(X)[0]
    )

    # Obtener probabilidad de depresión.
    probability = float(
        MODEL.predict_proba(X)[0][1]
    )

    # Obtener los valores SHAP correspondientes
    # a la clase positiva (depresión).
    if isinstance(shap_values, list):
        valores_shap = shap_values[1][0]
    else:
        valores_shap = shap_values[0, :, 1]

    nombres_variables = (
        PREPROCESSOR.get_feature_names_out()
    )

    # Crear resultado.
    variables = [
        {
            "variable": nombre,
            "valor": float(valor),
            "impacto_absoluto": round(
                abs(float(valor)),
                6
            ),
            "direccion": (
                "aumenta la probabilidad de depresión"
                if valor > 0
                else "disminuye la probabilidad de depresión"
            )
        }
        for nombre, valor in zip(
            nombres_variables,
            valores_shap
        )
    ]

    # Ordenar por magnitud del impacto.
    variables.sort(
        key=lambda x: x["impacto_absoluto"],
        reverse=True
    )

    return {
        "prediction": prediction,
        "probability_depression": round(
            probability,
            4
        ),
        "variables_importantes": variables
    }