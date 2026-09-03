"""
Interfaz web hecha con Streamlit para probar
la API del modelo de predicción de depresión
estudiantil, sin tener que usar Swagger o Postman.
"""

import os

import requests
import streamlit as st



# Configuración

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
)


st.set_page_config(
    page_title="Predicción de Depresión Estudiantil",
    page_icon="🧠",
    layout="centered"
)


st.title("Predicción de Depresión Estudiantil")

st.caption(
    f"Conectado a la API en: `{API_URL}`"
)

# Estado de la API

with st.sidebar:

    st.subheader("Estado de la API")

    try:

        resp = requests.get(
            API_URL,
            timeout=5
        )

        if resp.status_code == 200:

            data = resp.json()

            st.success(
                f"{data.get('status', 'running')} · "
                f"v{data.get('version', '?')}"
            )

        else:

            st.error(
                f"La API respondió con código "
                f"{resp.status_code}"
            )

    except requests.exceptions.RequestException:

        st.error(
            "No se pudo conectar con la API. "
            "¿Está corriendo?"
        )


# Pestañas

tab_individual, tab_masiva = st.tabs(
    [
        "🧍 Predicción individual",
        "📄 Predicción masiva (CSV/XLSX)"
    ]
)


# Predicción individual
# POST /predict
# POST /case-importance

with tab_individual:

    st.subheader("Datos del estudiante")

    with st.form("form_prediccion"):

        col1, col2 = st.columns(2)

        # Columna 1

        with col1:

            gender = st.selectbox(
                "Género",
                ["Male", "Female"],
                format_func=lambda v:
                    "Masculino"
                    if v == "Male"
                    else "Femenino"
            )

            age = st.number_input(
                "Edad",
                min_value=15,
                max_value=60,
                value=22
            )

            academic_pressure = st.slider(
                "Presión académica",
                0.0,
                5.0,
                3.0,
                0.5
            )

            cgpa = st.number_input(
                "CGPA",
                min_value=0.0,
                max_value=10.0,
                value=7.5,
                step=0.01
            )

            study_satisfaction = st.slider(
                "Satisfacción con los estudios",
                0.0,
                5.0,
                3.0,
                0.5
            )

            sleep_duration = st.selectbox(
                "Duración del sueño",
                [
                    "Less than 5 hours",
                    "5-6 hours",
                    "7-8 hours",
                    "More than 8 hours"
                ],
                format_func=lambda v: {
                    "Less than 5 hours":
                        "Menos de 5 horas",
                    "5-6 hours":
                        "5 a 6 horas",
                    "7-8 hours":
                        "7 a 8 horas",
                    "More than 8 hours":
                        "Más de 8 horas"
                }[v]
            )

        # Columna 2

        with col2:

            dietary_habits = st.selectbox(
                "Hábitos alimenticios",
                [
                    "Healthy",
                    "Moderate",
                    "Unhealthy"
                ],
                format_func=lambda v: {
                    "Healthy": "Saludables",
                    "Moderate": "Moderados",
                    "Unhealthy": "Poco saludables"
                }[v]
            )

            degree = st.text_input(
                "Título/Grado (ej: BSc, M.Tech, PhD)",
                value="BSc"
            )

            suicidal_thoughts = st.selectbox(
                "¿Ha tenido pensamientos suicidas?",
                ["Yes", "No"],
                format_func=lambda v:
                    "Sí"
                    if v == "Yes"
                    else "No"
            )

            work_study_hours = st.number_input(
                "Horas de trabajo/estudio diarias",
                min_value=0.0,
                max_value=24.0,
                value=8.0
            )

            financial_stress = st.slider(
                "Estrés financiero",
                0.0,
                5.0,
                3.0,
                0.5
            )

            family_history = st.selectbox(
                "Historial familiar de enfermedad mental",
                ["Yes", "No"],
                format_func=lambda v:
                    "Sí"
                    if v == "Yes"
                    else "No"
            )

        submitted = st.form_submit_button(
            "🔍 Predecir"
        )


    # Ejecutar predicción

    if submitted:

        payload = {
            "Gender": gender,
            "Age": age,
            "Academic_Pressure": academic_pressure,
            "CGPA": cgpa,
            "Study_Satisfaction": study_satisfaction,
            "Sleep_Duration": sleep_duration,
            "Dietary_Habits": dietary_habits,
            "Degree": degree,
            "Suicidal_Thoughts": suicidal_thoughts,
            "Work_Study_Hours": work_study_hours,
            "Financial_Stress": financial_stress,
            "Family_History_Mental_Illness": family_history
        }

        try:

            # POST /predict

            r_predict = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=15
            )

            r_predict.raise_for_status()

            result = r_predict.json()

            prediction = result["prediction"]

            probability = result[
                "probability_depression"
            ]


            # Resultado

            st.divider()

            st.subheader(
                "Resultado de la predicción"
            )

            if prediction == 1:

                st.error(
                    "⚠️ Posible caso de depresión\n\n"
                    f"Probabilidad estimada: "
                    f"{probability:.2%}"
                )

            else:

                st.success(
                    "✅ No presenta indicios de depresión\n\n"
                    f"Probabilidad estimada: "
                    f"{probability:.2%}"
                )

            st.progress(
                min(
                    max(probability, 0.0),
                    1.0
                )
            )


            # POST /case-importance

            with st.spinner(
                "Analizando las variables que influyeron "
                "en la predicción..."
            ):

                r_importance = requests.post(
                    f"{API_URL}/case-importance",
                    json=payload,
                    timeout=30
                )

                r_importance.raise_for_status()

                importance_result = (
                    r_importance.json()
                )


            # Mostrar importancia de las variables

            variables = importance_result.get(
                "variables_importantes",
                []
            )

            st.divider()

            st.subheader(
                "🔍 Variables más importantes para este caso"
            )

            if variables:

                st.caption(
                    "Estas variables representan los factores "
                    "que más influyeron en la predicción del "
                    "modelo para este caso específico."
                )

                for variable in variables[:10]:

                    nombre = variable["variable"]

                    impacto = variable[
                        "impacto_absoluto"
                    ]

                    direccion = variable[
                        "direccion"
                    ]

                    col_nombre, col_impacto = (
                        st.columns([3, 1])
                    )

                    with col_nombre:

                        st.write(
                            f"**{nombre}**"
                        )

                        st.caption(
                            direccion
                        )

                    with col_impacto:

                        st.metric(
                            "Impacto",
                            f"{impacto:.4f}"
                        )

                    # Normalización visual para la barra.
                    st.progress(
                        min(
                            impacto * 5,
                            1.0
                        )
                    )

            else:

                st.warning(
                    "No se encontraron variables de importancia "
                    "para este caso."
                )


        except requests.exceptions.RequestException as e:

            st.error(
                f"Error al consultar la API: {e}"
            )


# Predicción masiva
# POST /predict-file

with tab_masiva:

    st.subheader(
        "Subir dataset (CSV o XLSX)"
    )

    st.caption(
        "El archivo debe contener las mismas columnas "
        "utilizadas durante el entrenamiento."
    )

    uploaded_file = st.file_uploader(
        "Selecciona un archivo",
        type=["csv", "xlsx"]
    )

    if (
        uploaded_file is not None
        and st.button("Procesar archivo")
    ):

        try:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            r = requests.post(
                f"{API_URL}/predict-file",
                files=files,
                timeout=60
            )

            r.raise_for_status()

            extension = os.path.splitext(
                uploaded_file.name
            )[1].lower()

            mime = (
                "text/csv"
                if extension == ".csv"
                else (
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                )
            )

            st.success(
                "Predicciones generadas correctamente."
            )

            st.download_button(
                label="⬇️ Descargar resultados",
                data=r.content,
                file_name=f"predictions{extension}",
                mime=mime
            )

        except requests.exceptions.RequestException as e:

            st.error(
                f"Error al consultar la API: {e}"
            )