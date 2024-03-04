# Usa una imagen de Python como base
FROM python:3.8-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Crea un directorio para la base de datos y establece los permisos adecuados
RUN mkdir /app/data && chown -R nobody:nogroup /app/data

# Copia los archivos necesarios al contenedor
COPY requirements.txt /app/requirements.txt
COPY src /app/src
COPY start_server.sh /app/start_server.sh
RUN chmod +x /app/start_server.sh 

# Instala las dependencias
RUN pip install -r requirements.txt

# Asegúrate de que el usuario nobody pueda escribir en el directorio de la base de datos
USER nobody

