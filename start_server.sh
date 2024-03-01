#!/bin/bash

# Establecer el entorno de Flask a desarrollo para habilitar el modo de depuración
export FLASK_ENV=development

# Establecer el archivo que Flask debería ejecutar
export FLASK_APP=src/main.py

# Establece el host para flask run
export FLASK_RUN_HOST=0.0.0.0

# Iniciar el servidor Flask en el puerto 8081
flask run --port=8081
