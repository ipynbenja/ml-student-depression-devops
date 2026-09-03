# Registro de cambios

Todas las modificaciones notables de este proyecto serán documentadas en este archivo. Esto refiere a todo lo que afecte cómo se entiende, ejecuta y/o instala el proyecto.

## - 2026-08-28

### Añadido
- Se añadió documentación CHANGELOG.md para la documentación de cambios notables.
- Se añadió el archivo YAML para el workflow de Integración Continua (CI) que se ejecutará por cada push o pull request realizado a la rama main.

### Cambiado
- Se actualizó la documentación README.md para esta nueva versión del proyecto, donde el propósito es integrar prácticas de la cultura DevOps, se define nuevo objetivo, estrategia de ramas y commits.

## - 2026-08-31

### Añadido
- Se añadió un entorno de testing para realizar pruebas unitarias a la API utilizando `pytest` y `TestClient` para los endpoints de la API (`/`, `/predict` y `/predict-file`).
- Se esperará aprobación del docente para antes de integrar las pruebas en el workflow CI para su ejecución automática. 

### Cambiado
- Se añadieron filtros de exclusión (`paths-ignore`) en GitHub Actions para omitir la ejecución del pipeline en cambios exclusivos de documentación (para cualquier archvio .md)
- Actualizaciones pequeñas en .gitignore y requirements.txt para las pruebas unitarias

### Corregido
- Error en una fecha de este documento.

## - 2026-09-01

### Añadido
- Se añadió una interfaz web con streamlit (streamlit_app.py) para probar la API sin depender de Swagger o Postman, con un formulario para predicción individual y carga de archivos CSV/XLSX para predicción masiva.

- Se agregaron streamlit y requests a requirements.txt como dependencias de la interfaz web.

- Se añadió la dependencia shap==0.48.0 al archivo requirements.txt para permitir la interpretación de predicciones individuales del modelo Random Forest.

- Se añadió el endpoint POST /importancia-caso, destinado a obtener la importancia individual de las variables para un caso específico mediante SHAP.

- Se añadió una función para obtener explicaciones individuales de las predicciones utilizando shap.TreeExplainer.

### Cambiado
- Se actualizó la obtención de la importancia de las variables para considerar correctamente la estructura del modelo almacenado como un Pipeline, accediendo al modelo Random Forest mediante MODEL.named_steps["model"].

- Se actualizó el proceso de interpretación de variables para utilizar los nombres generados por el preprocesador mediante PREPROCESSOR.get_feature_names_out().

- Se amplió la respuesta de las predicciones individuales para incluir la probabilidad de depresión y la dirección del impacto de las variables identificadas mediante SHAP.

### Corregido
- Se corrigió el acceso a las características de importancia del Random Forest, debido a que el archivo random_forest_model.pkl contiene un Pipeline con el modelo almacenado en el paso model.

## - 2026-09-02

### Añadido

* Se agregó al archivo `streamlit_app.py` la capacidad de consumir el endpoint `POST /case-importance`, permitiendo mostrar en la interfaz web la importancia de las variables que influyeron en el análisis de un usuario.

### Cambiado

* Se refactorizó la ubicación del archivo `streamlit_app.py`, trasladándolo desde la raíz del proyecto a la carpeta `frontend`, con el objetivo de mejorar la organización de los componentes del proyecto.

* Se modificó la estructura del archivo `Dockerfile` para permitir la ejecución simultánea de la API mediante `main.py` y de la interfaz web mediante `streamlit_app.py`.

### Corregido

* Se eliminó una función importada en la API `main.py` que no estaba siendo utilizada.

* Se eliminó el archivo `test.py` de la carpeta `frontend`, debido a que no aportaba funcionalidad al proyecto.