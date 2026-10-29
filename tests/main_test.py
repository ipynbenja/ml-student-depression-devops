
import io
from unittest.mock import patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

#DATOS DE PRUEBA (PAYLOAD)
VALID_STUDENT_PAYLOAD = {
    "Gender": "Male",
    "Age": 20.0,
    "Academic_Pressure": 4.0,
    "CGPA": 3.5,
    "Study_Satisfaction": 3.0,
    "Sleep_Duration": "5-6 hours",
    "Dietary_Habits": "Moderate",
    "Degree": "B.Tech",
    "Suicidal_Thoughts": "No",
    "Work_Study_Hours": 6.0,
    "Financial_Stress": 3.0,
    "Family_History_Mental_Illness": "No",
}

#1. PRUEBA DE ENDPOINT RAÍZ Y SALUD
def test_root():
    """Prueba el endpoint raíz para verificar que la API está corriendo."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["version"] == "1.0.0"


#2. PRUEBAS DE PREDICCIÓN INDIVIDUAL (/predict)
@patch("api.main.predecir_estudiante")
def test_predict_individual_success(mock_predecir):
    """Flujo exitoso de predicción individual (Caso Positivo)"""
    #Configuramos qué queremos que devuelva el mock
    mock_predecir.return_value = {"prediction": 1, "probability_depression": 0.78}

    response = client.post("/predict", json=VALID_STUDENT_PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {"prediction": 1, "probability_depression": 0.78}
    mock_predecir.assert_called_once()


def test_predict_missing_required_field():
    """Validación de Pydantic cuando falta un campo obligatorio (Falla 422)"""
    payload_incompleto = VALID_STUDENT_PAYLOAD.copy()
    del payload_incompleto["Gender"] #Quitamos el género en el payload 

    response = client.post("/predict", json=payload_incompleto)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


@pytest.mark.parametrize(
    "campo_invalido,valor_invalido",
    [
        ("Age", "veinte"),  #Debería ser numérico
        ("Work_Study_Hours", "ocho horas"),  #Debería ser numérico
    ],
)
def test_predict_invalid_data_types(campo_invalido, valor_invalido):
    """Validación de Pydantic con tipos de datos incorrectos (Falla 422)."""
    payload_invalido = VALID_STUDENT_PAYLOAD.copy()
    payload_invalido[campo_invalido] = valor_invalido

    response = client.post("/predict", json=payload_invalido)

    assert response.status_code == 422



#3. PRUEBAS DE IMPORTANCIA DEL CASO (/case-importance)
@patch("api.main.obtener_importancia_caso")
def test_case_importance_success(mock_importancia):
    """Flujo exitoso para la importancia de variables."""
    mock_importancia.return_value = {
        "variables_importantes": [
            {
                "variable": "Academic_Pressure",
                "impacto_absoluto": 0.25,
                "direccion": "Aumenta riesgo",
            }
        ]
    }

    response = client.post("/case-importance", json=VALID_STUDENT_PAYLOAD)

    assert response.status_code == 200
    assert "variables_importantes" in response.json()


@patch("api.main.obtener_importancia_caso")
def test_case_importance_model_error(mock_importancia):
    """Manejo de error interno cuando el cálculo de importancia falla (500 Error)."""
    mock_importancia.side_effect = RuntimeError("Error interno del modelo SHAP/RandomForest")

    response = client.post("/case-importance", json=VALID_STUDENT_PAYLOAD)

    assert response.status_code == 500
    assert "Error al obtener la importancia" in response.json()["detail"]


#4. PRUEBAS DE PREDICCIÓN MASIVA (/predict-file)
def test_predict_file_invalid_extension():
    """Rechazar formatos no permitidos (por ejemplo .txt)."""
    fake_file = io.BytesIO(b"Archivo no permitido")

    response = client.post("/predict-file", files={"file": ("test.txt", fake_file, "text/plain")})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Solo se permiten archivos CSV o XLSX."
    }


@patch("api.main.predecir_dataframe")
def test_predict_file_csv(mock_predecir_df):
    """Prueba el endpoint de subida de CSV válido."""
    mock_predecir_df.return_value = pd.DataFrame({"Gender": ["Male"], "prediccion": [1]})

    csv_content = (
        b"Sleep Duration,Have you ever had suicidal thoughts ?,Work/Study Hours,"
        b"Study Satisfaction,Degree,Financial Stress,Academic Pressure,Gender,"
        b"CGPA,Age,Dietary Habits,Family History of Mental Illness\n"
        b"5-6 hours,No,6,3,B.Tech,3,4,Male,3.5,20,Moderate,No\n"
    )
    fake_file = io.BytesIO(csv_content)

    response = client.post(
        "/predict-file",
        files={"file": ("estudiantes.csv", fake_file, "text/csv")}
    )

    assert response.status_code == 200 #Se espera una respuesta 200 (OK)
    assert response.headers["content-type"] == "application/octet-stream" #Se espera recibir un archivo binario
    mock_predecir_df.assert_called_once() #Se espera que sea llamado una vez


@patch("api.main.predecir_dataframe")
def test_predict_file_xlsx_success(mock_predecir_df):
    """Procesamiento correcto de un archivo Excel XLSX válido."""
    mock_predecir_df.return_value = pd.DataFrame(
        {"Gender": ["Female"], "prediction": [0], "probability_depression": [0.12]}
    )

    df_test = pd.DataFrame([{
        "Sleep Duration": "5-6 hours",
        "Have you ever had suicidal thoughts ?": "No",
        "Work/Study Hours": 6.0,
        "Study Satisfaction": 3.0,
        "Degree": "B.Tech",
        "Financial Stress": 3.0,
        "Academic Pressure": 4.0,
        "Gender": "Female",
        "CGPA": 3.5,
        "Age": 20.0,
        "Dietary Habits": "Moderate",
        "Family History of Mental Illness": "No",
    }])
    excel_buffer = io.BytesIO()
    df_test.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    response = client.post(
        "/predict-file",
        files={"file": ("estudiantes.xlsx", excel_buffer, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",)},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    mock_predecir_df.assert_called_once()


@patch("api.main.predecir_dataframe")
def test_predict_file_empty_csv(mock_predecir_df):
    """Manejo de archivo CSV vacío devolviendo un error controlado."""
    fake_file = io.BytesIO(b"")

    response = client.post("/predict-file", files={"file": ("vacio.csv", fake_file, "text/csv")},)

    #Verificamos que responda limpiamente con el JSON de error
    assert response.status_code == 400
    assert response.json() == {"detail": "El archivo está vacío."}
