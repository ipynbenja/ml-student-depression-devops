from fastapi.testclient import TestClient
from unittest.mock import patch
import pandas as pd
import io
from api.main import app

client = TestClient(app)

def test_root():
    """Prueba el endpoint raíz para verificar que la API está corriendo."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running" #Se comprueba que el estado sea running
    assert data["version"] == "1.0.0" #Se comprueba que la versión sea 1.0.0


@patch("api.main.predecir_estudiante")
def test_predict_individual(mock_predecir):
    """Prueba el endpoint de predicción individual simulando la respuesta del modelo."""
    #Configuramos qué queremos que devuelva el mock
    mock_predecir.return_value = {"prediccion": 1, "probabilidad": 0.78}

    #Creamos una variable payload simulando lo que espera StudentRequest
    payload = {
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
        "Family_History_Mental_Illness": "No"
    }

    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200 #Se espera una respuesta 200 (OK)
    assert response.json() == {"prediccion": 1, "probabilidad": 0.78} #Se espera que el resultado coincida
    mock_predecir.assert_called_once() #Se espera que sea llamado una vez


def test_predict_file_invalid_extension():
    """Prueba que la API rechace archivos que no sean CSV o XLSX."""
    #Creamos un archivo falso de texto plano (txt)
    fake_file = io.BytesIO(b"Este archivo no deberia pasar la prueba")
    
    response = client.post(
        "/predict-file",
        files={"file": ("test.txt", fake_file, "text/plain")}
    )
    
    assert response.status_code == 200 #Se espera una respuesta 200 (OK)
    assert response.json() == {"error": "Solo se permiten archivos CSV o XLSX"} #Se espera que el mensaje sea de error


@patch("api.main.predecir_dataframe")
def test_predict_file_csv(mock_predecir_df):
    """Prueba el endpoint de subida de CSV simulando el procesamiento por lotes."""
    mock_predecir_df.return_value = pd.DataFrame({"Gender": ["Male"], "prediccion": [1]})

    csv_content = b"""Gender,Age,Academic_Pressure,CGPA,Study_Satisfaction,Sleep_Duration,Dietary_Habits,Degree,Suicidal_Thoughts,Work_Study_Hours,Financial_Stress,Family_History_Mental_Illness
    Male,20,4,3.5,3,5-6 hours,Moderate,B.Tech,No,6,3,No\n"""
    fake_file = io.BytesIO(csv_content)

    response = client.post(
        "/predict-file",
        files={"file": ("estudiantes.csv", fake_file, "text/csv")}
    )

    assert response.status_code == 200 #Se espera una respuesta 200 (OK)
    assert response.headers["content-type"] == "application/octet-stream" #Se espera recibir un archivo binario
    mock_predecir_df.assert_called_once() #Se espera que sea llamado una vez