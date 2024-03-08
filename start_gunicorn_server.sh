#!/bin/bash

# Establece el número de workers para Gunicorn (ajustar según la potencia del servidor)
NUM_WORKERS=1

# Establece el nombre de la aplicación, asumiendo que `main.py` es tu archivo y `app` es tu instancia de la aplicación Flask
APP_NAME="src.main:app"

# Ejecuta Gunicorn en el puerto 8081 y enlaza a 0.0.0.0 para que esté accesible fuera del contenedor
exec gunicorn --workers=$NUM_WORKERS --bind=0.0.0.0:8081 --pythonpath src $APP_NAME
