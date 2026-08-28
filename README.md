# proyecto-ml-student-depression-devops

# Microservicio: Predicción de Depresión Estudiantil (MLOps / DevOps Pipeline)

> **Asignatura:** Ingeniería DevOps (DOY0101)  

> **Institución:** Duoc UC  

> **Integrantes:** Abel Aravena, Benjamín Aravena, Benjamín Tapia

## Descripción del microservicio

Este microservicio corresponde a un modelo de Machine Learning desarrollado en una aisgnatura anterior, orientado a la detección de indicadores de depresión en estudiantes de educación superior. En esta primera fase del ciclo DevOps, se ha configurado la infraestructura base de control de versiones, flujos de trabajo colaborativos y un pipeline automatizado mediante GitHub Actions.

---

## Estrategia de ramificación 

Para este microservicio hemos elegido **Trunk-Based Development (TBD)** debido a las siguientes razones clave en un proyecto de Machine Learning:

- En modelos de Machine Learning y APIs, integrar cambios pequeños constantemente permite validar que el modelo, las dependencias y la API sigan funcionando sin romper el sistema.
- Optamos por el uso de ramas de corta duración, y así integramos cambios de forma fluida hacia la rama principal (main) sin sufrir colisiones de código masivas.
- TBD en futuras versiones también complementará directamente el flujo de Integración Continua (CI), ejecutando pruebas automáticas en cada **Pull Request** antes de fusionar.

---

### Commits convencionales 

Adoptamos el estándar **Conventional Commits** para garantizar la trazabilidad del código: 

-`feat:` Nuevas funcionalidades o endpoints (ej. `feat: agregar endpoint de predicción`). 

-`fix:` Corrección de errores o bugs (ej. `fix: corregir tipo de dato en entrada del modelo`). 

-`hotfix:` Corrección **urgente** de errores o bugs (ej. `hotfix: solución de login para usuarios`)

-`docs:` Cambios exclusivamente en documentación (ej. `docs: actualizar guía de instalación`). 

-`ci:` Cambios en la configuración de GitHub Actions (ej. `ci: agregar paso de pytest`). 

-`refactor:` Refactorización de código sin alterar la funcionalidad previa.

# Student Depression Prediction API

API REST desarrollada con **FastAPI** y **Scikit-Learn** para predecir posibles casos de depresión estudiantil utilizando un modelo de Machine Learning entrenado previamente.

La aplicación se encuentra completamente dockerizada para facilitar su despliegue en cualquier entorno.

---

## Funcionalidades

La API permite:

* Realizar predicciones individuales mediante JSON.
* Procesar datasets completos en formato CSV o XLSX.
* Aplicar automáticamente el pipeline de preprocesamiento utilizado durante el entrenamiento.
* Obtener probabilidades de depresión estudiantil.
* Descargar archivos con predicciones generadas.
* Ejecutarse dentro de un contenedor Docker.

---

## Tecnologías utilizadas

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

## Estructura del proyecto

```text
ml-student-depression-devops
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

## Construcción de la imagen Docker

```bash
docker build -t student-depression-api .
```

---

## Ejecución del contenedor

```bash
docker run -p 8000:8000 student-depression-api
```

La API quedará disponible en:

```text
http://localhost:8000
```

---

## Documentación Swagger

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

## Prueba rápida con Postman

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

## Dependencias principales

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

## Consideraciones

* El modelo Random Forest y el preprocesador se cargan una única vez al iniciar la API.
* Las predicciones utilizan exactamente el mismo pipeline empleado durante el entrenamiento.
* Los archivos CSV y XLSX deben contener las mismas columnas utilizadas durante la etapa de entrenamiento.
* Swagger se encuentra disponible automáticamente mediante FastAPI.
* El proyecto puede desplegarse en Docker, servidores Linux, servicios cloud o Kubernetes.

---

## Arquitectura de inferencia

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
