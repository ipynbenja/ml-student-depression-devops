# Project-data-science-3-Docker

# 🧠 Student Depression Prediction API

API REST desarrollada con **FastAPI** y **Scikit-Learn** para predecir posibles casos de depresión estudiantil utilizando un modelo de Machine Learning entrenado previamente.

La aplicación se encuentra completamente dockerizada para facilitar su despliegue en cualquier entorno.

---

## 📌 Descripción

La API permite:

* Realizar predicciones individuales mediante JSON.
* Procesar datasets completos en formato CSV o XLSX.
* Aplicar automáticamente el pipeline de preprocesamiento utilizado durante el entrenamiento.
* Obtener probabilidades de depresión estudiantil.
* Descargar archivos con predicciones generadas.
* Ejecutarse dentro de un contenedor Docker.

---

## 🧠 Tecnologías utilizadas

* Python 3.12
* FastAPI
* Uvicorn
* Pandas
* NumPy
* Scikit-Learn
* Category Encoders
* Joblib
* Docker

---

## 📂 Estructura del proyecto

```text
Project-data-science-3-Docker
│
├── api/
│   └── main.py
│
├── Request/
│   └── StudentRequest.py
│
├── src/
│   ├── model_utils.py
│   └── carga_csv.py
│
├── models/
│   ├── random_forest_model.pkl
│   └── preprocessor.pkl
│
├── data/
│   └── Student_Depression_Dataset_Prediction.csv
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🚀 Construcción de la imagen Docker

```bash
docker build -t student-depression-api .
```

---

## ▶️ Ejecución del contenedor

```bash
docker run -p 8000:8000 student-depression-api
```

La API quedará disponible en:

```text
http://localhost:8000
```

---

## 📖 Documentación Swagger

FastAPI genera automáticamente documentación interactiva.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

# Endpoints

## GET /

Verifica que la API esté operativa.

### Respuesta

```json
{
  "message": "Student Depression Prediction API",
  "status": "running",
  "version": "1.0.0"
}
```

---

## POST /predict

Realiza una predicción individual.

### Request Body

```json
{
  "Gender": "Male",
  "Age": 22,
  "Academic_Pressure": 4,
  "CGPA": 7.5,
  "Study_Satisfaction": 3,
  "Sleep_Duration": "5-6 hours",
  "Dietary_Habits": "Moderate",
  "Degree": "B.Tech",
  "Suicidal_Thoughts": "Yes",
  "Work_Study_Hours": 8,
  "Financial_Stress": 4,
  "Family_History_Mental_Illness": "Yes"
}
```

### Respuesta

```json
{
  "prediction": 1,
  "probability_depression": 0.8421
}
```

### Interpretación

| Valor | Significado                       |
| ----- | --------------------------------- |
| 0     | No presenta indicios de depresión |
| 1     | Posible caso de depresión         |

---

## POST /predict-file

Permite realizar predicciones masivas sobre datasets completos.

### Formatos soportados

* CSV (.csv)
* Excel (.xlsx)

### Ejemplo usando cURL

```bash
curl -X POST \
  "http://localhost:8000/predict-file" \
  -F "file=@Student_Depression_Dataset_Prediction.csv"
```

### Resultado

La API devuelve un archivo con dos columnas adicionales:

```text
Prediction
Probability_Depression
```

---

## 🧪 Prueba rápida con Postman

### URL

```text
POST http://localhost:8000/predict
```

### Headers

```text
Content-Type: application/json
```

### Body (raw → JSON)

```json
{
  "Gender": "Female",
  "Age": 20,
  "Academic_Pressure": 5,
  "CGPA": 8.2,
  "Study_Satisfaction": 2,
  "Sleep_Duration": "Less than 5 hours",
  "Dietary_Habits": "Unhealthy",
  "Degree": "B.Sc",
  "Suicidal_Thoughts": "No",
  "Work_Study_Hours": 10,
  "Financial_Stress": 5,
  "Family_History_Mental_Illness": "No"
}
```

---

## 📦 Dependencias principales

```text
pandas==3.0.3
numpy==2.4.5
joblib==1.5.3
scikit-learn==1.9.0
category_encoders==2.8.1

fastapi==0.116.1
uvicorn[standard]==0.35.0
pydantic==2.11.7

python-multipart==0.0.20
openpyxl==3.1.5
```

---

## ⚠️ Consideraciones

* El modelo Random Forest y el preprocesador se cargan una única vez al iniciar la API.
* Las predicciones utilizan exactamente el mismo pipeline empleado durante el entrenamiento.
* Los archivos CSV y XLSX deben contener las mismas columnas utilizadas durante la etapa de entrenamiento.
* Swagger se encuentra disponible automáticamente mediante FastAPI.
* El proyecto puede desplegarse en Docker, servidores Linux, servicios cloud o Kubernetes.

---

## 🏗️ Arquitectura de inferencia

```text
Request
   │
   ▼
FastAPI
   │
   ▼
StudentRequest
   │
   ▼
model_utils.py
   │
   ├── crear_dataframe_prediccion()
   ├── transformar_dataset()
   └── predecir_estudiante()
   │
   ▼
Preprocessor.pkl
   │
   ▼
RandomForestModel.pkl
   │
   ▼
Response JSON
```

---
