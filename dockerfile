# Imagen base de Python 3.12 basada en Debian 12
FROM python:3.12-slim-bookworm

WORKDIR /app

# Actualizar los paquetes del sistema e instalar dependencias Python
COPY requirements.txt .

RUN apt-get update \
    && apt-get upgrade -y \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar el código de la aplicación
COPY . .

# Puerto de FastAPI y puerto de Streamlit
EXPOSE 8000
EXPOSE 8501

# Iniciar la API y la interfaz
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_app.py --server.address 0.0.0.0 --server.port 8501"]