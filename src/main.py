from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime, timedelta
import random
from database import DatabaseManager, User, Ingredient, Bocadillo, Pedido  # Asegura que esto coincida con tus nombres de importación

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
db_manager = DatabaseManager()

@app.route('/')
def home():
    usuarios = db_manager.get_all_users()
    bocadillos = db_manager.get_all_bocadillos()
    pedidos = db_manager.get_pedidos_de_hoy()
    return render_template('index.html', usuarios=usuarios, bocadillos=bocadillos, pedidos=pedidos)


@app.route('/profile')
def profile():
    usuarios = db_manager.get_all_users()  # Obtiene todos los usuarios
    usuarios_y_consumo = []

    for usuario in usuarios:
        consumo_data = db_manager.get_consumo_usuario_por_fecha(usuario.usuario_id)
        # Combina el usuario y sus datos de consumo en un diccionario
        usuario_con_consumo = {
            "usuario": usuario,
            "consumo_data": consumo_data
        }
        usuarios_y_consumo.append(usuario_con_consumo)

    return render_template('profile.html', usuarios_y_consumo=usuarios_y_consumo)




@app.route('/admin', methods=['GET'])
def admin():
    users = db_manager.get_all_users()
    ingredients = db_manager.get_all_ingredients()
    bocadillos = db_manager.get_all_bocadillos()
    hoy = datetime.now().strftime('%Y-%m-%d')
    return render_template('admin.html', users=users, ingredients=ingredients, bocadillos=bocadillos, hoy=hoy )

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


@app.route('/admin/crear-bocadillo', methods=['POST'])
def crear_bocadillo():
    nombre_bocadillo = request.form['nombreBocadillo']
    ingredientes_ids = request.form.getlist('ingredientes')  # Esto captura los IDs de los ingredientes seleccionados
    nuevo_bocadillo = Bocadillo(nombre=nombre_bocadillo)
    db_manager.insert_bocadillo(nuevo_bocadillo, ingredientes_ids)
    return redirect(url_for('admin'))
 
 
@app.route('/admin/editar-bocadillo/<int:bocadillo_id>', methods=['GET', 'POST'])
def editar_bocadillo(bocadillo_id):
    if request.method == 'POST':
        nombre_bocadillo = request.form['nombreBocadillo']
        ingredientes_ids = request.form.getlist('ingredientes')  # IDs de los ingredientes seleccionados
        
        # Suponiendo que tienes una manera de crear/actualizar un objeto Bocadillo
        bocadillo_actualizado = Bocadillo(nombre=nombre_bocadillo, bocadillo_id=bocadillo_id)
        db_manager.update_bocadillo(bocadillo_actualizado, ingredientes_ids)
        
        return redirect(url_for('admin'))
    else:
        bocadillo = db_manager.get_bocadillo_by_id(bocadillo_id) 
        todos_ingredientes = db_manager.get_all_ingredients()  # Para listar en el formulario
        return render_template('editar_bocadillo.html', bocadillo=bocadillo, todos_ingredientes=todos_ingredientes)


@app.route('/admin/borrar-bocadillo/<int:bocadillo_id>')
def borrar_bocadillo(bocadillo_id):
    db_manager.delete_bocadillo(bocadillo_id)
    return redirect(url_for('admin'))



@app.route('/registrar-pedido', methods=['POST'])
def registrar_pedido():
    usuario_id = request.form['usuario_id']
    bocadillo_id = request.form['bocadillo_id']
    db_manager.insertar_pedido(usuario_id, bocadillo_id)
    return redirect(url_for('home'))

@app.route('/borrar-pedido/<int:registro_id>')
def borrar_pedido(registro_id):
    db_manager.borrar_pedido(registro_id)  # Asume que este método existe en db_manager
    return redirect(url_for('home'))
