from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime, timedelta
import random
import database as db

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def initialize_app():
    db.init_db()
    


@app.route('/')
def home():
    return render_template('index.html')


# Generar datos de uso para los últimos 365 días
start_date = datetime.now() - timedelta(days=365)
usage_data = {
    (start_date + timedelta(days=i)).strftime('%Y-%m-%d'): random.randint(0, 10)
    for i in range(365)
}

@app.route('/profile')
def profile():
    # Pasar los datos de uso a la plantilla
    return render_template('profile.html', usage_data=usage_data)

@app.route('/admin', methods=['GET'])
def admin():
    users = db.get_all_users()
    ingredients = db.get_all_ingredients()
    return render_template('admin.html', users=users, ingredients=ingredients)


@app.route('/admin/crear-usuario', methods=['POST'])
def crear_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    fecha_registro = request.form['fechaRegistro']
    
    # Aquí insertarías los datos en la base de datos usando la función que definiste para ello.
    # Por ejemplo:
    db.insert_user(nombre, email, fecha_registro)
    
    # Redirige a otra página tras insertar el usuario, por ejemplo, a la página de administración.
    return redirect(url_for('admin'))

@app.route('/admin/crear-ingrediente', methods=['POST'])
def crear_ingrediente():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    
    # Aquí insertarías los datos en la base de datos.
    # Suponiendo que tienes una función insert_ingredient(nombre, descripcion) definida en database.py
    db.insert_ingredient(nombre, descripcion)
    
    # Redirigir a otra página, por ejemplo, a la página principal de administración tras añadir el ingrediente.
    return redirect(url_for('admin'))



@app.route('/admin/editar-usuario/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    if request.method == 'POST':
        # Aquí procesarías los datos enviados desde el formulario de edición
        nombre = request.form['nombre']
        email = request.form['email']
        fecha_registro = request.form['fechaRegistro']
        # Actualiza el usuario en la base de datos
        db.update_user(user_id, nombre, email, fecha_registro)
        return redirect(url_for('admin'))
    else:
        # Obtén los detalles del usuario para mostrarlos en el formulario de edición
        user = db.get_user_by_id(user_id)
        return render_template('editar_usuario.html', user=user)

@app.route('/admin/borrar-usuario/<int:user_id>')
def borrar_usuario(user_id):
    db.delete_user(user_id)
    return redirect(url_for('admin'))

# Repite patrones similares para editar y borrar ingredientes
@app.route('/admin/editar-ingrediente/<int:ingrediente_id>', methods=['GET', 'POST'])
def editar_ingrediente(ingrediente_id):
    if request.method == 'POST':
        # Procesar los datos enviados desde el formulario de edición
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        # Actualiza el ingrediente en la base de datos
        db.update_ingredient(ingrediente_id, nombre, descripcion)
        return redirect(url_for('admin'))  # Asume que 'admin' es la función/ruta de tu página de administración
    else:
        # Obtén los detalles del ingrediente para mostrarlos en el formulario de edición
        ingrediente = db.get_ingrediente_by_id(ingrediente_id)
        return render_template('editar_ingrediente.html', ingrediente=ingrediente)


@app.route('/admin/borrar-ingrediente/<int:ingrediente_id>')
def borrar_ingrediente(ingrediente_id):
    db.delete_ingredient(ingrediente_id)
    return redirect(url_for('admin'))




initialize_app()