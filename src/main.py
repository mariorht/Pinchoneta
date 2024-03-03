from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime, timedelta
import random
from database import DatabaseManager, User, Ingredient  # Asegura que esto coincida con tus nombres de importación

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
db_manager = DatabaseManager()
db_manager.ensure_database()

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
    users = db_manager.get_all_users()
    ingredients = db_manager.get_all_ingredients()
    return render_template('admin.html', users=users, ingredients=ingredients)

@app.route('/admin/crear-usuario', methods=['POST'])
def crear_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    fecha_registro = request.form['fechaRegistro']
    new_user = User(nombre=nombre, email=email, fecha_registro=fecha_registro)
    db_manager.insert_user(new_user)
    return redirect(url_for('admin'))

@app.route('/admin/crear-ingrediente', methods=['POST'])
def crear_ingrediente():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    new_ingredient = Ingredient(nombre=nombre, descripcion=descripcion)
    db_manager.insert_ingredient(new_ingredient)
    return redirect(url_for('admin'))

@app.route('/admin/editar-usuario/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        fecha_registro = request.form['fechaRegistro']
        user_to_update = User(usuario_id=user_id, nombre=nombre, email=email, fecha_registro=fecha_registro)
        db_manager.update_user(user_to_update)
        return redirect(url_for('admin'))
    else:
        user = db_manager.get_user_by_id(user_id)
        return render_template('editar_usuario.html', user=user)

@app.route('/admin/borrar-usuario/<int:user_id>')
def borrar_usuario(user_id):
    db_manager.delete_user(user_id)
    return redirect(url_for('admin'))

@app.route('/admin/editar-ingrediente/<int:ingrediente_id>', methods=['GET', 'POST'])
def editar_ingrediente(ingrediente_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        ingredient_to_update = Ingredient(ingrediente_id=ingrediente_id, nombre=nombre, descripcion=descripcion)
        db_manager.update_ingredient(ingredient_to_update)
        return redirect(url_for('admin'))
    else:
        ingrediente = db_manager.get_ingredient_by_id(ingrediente_id)
        return render_template('editar_ingrediente.html', ingrediente=ingrediente)

@app.route('/admin/borrar-ingrediente/<int:ingrediente_id>')
def borrar_ingrediente(ingrediente_id):
    db_manager.delete_ingredient(ingrediente_id)
    return redirect(url_for('admin'))


