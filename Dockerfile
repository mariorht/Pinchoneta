# Usa una imagen de Python como base
FROM python:3.8-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt /app/requirements.txt
COPY src /app/src
COPY start_server.sh /app/start_server.sh

# Instala las dependencias
RUN pip install -r requirements.txt

