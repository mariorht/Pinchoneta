import sqlite3
import os

class User:
    def __init__(self, nombre, email, fecha_registro, usuario_id=None):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.email = email
        self.fecha_registro = fecha_registro


class Ingredient:
    def __init__(self, nombre, descripcion, ingrediente_id=None):
        self.ingrediente_id = ingrediente_id
        self.nombre = nombre
        self.descripcion = descripcion




class DatabaseManager:
    DATABASE_PATH = 'src/db/pinchonetaDB.db'
    SQL_SCRIPT_PATH = 'src/db/empty_bbdd.sql'

    def __init__(self):
        self.ensure_database()

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DatabaseManager.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def ensure_database():
        if not os.path.exists(DatabaseManager.DATABASE_PATH):
            print("No existe base de datos, se crea una vacía")
            os.makedirs(os.path.dirname(DatabaseManager.DATABASE_PATH), exist_ok=True)
            DatabaseManager.create_db_from_sql(DatabaseManager.SQL_SCRIPT_PATH)
        else:
            print("Ya existe base de datos")

    @staticmethod
    def create_db_from_sql(sql_file_path):
        with open(sql_file_path, 'r') as sql_file:
            sql_script = sql_file.read()
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()

    def insert_user(self, user):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (Nombre, Email, FechaRegistro) VALUES (?, ?, ?)", 
                       (user.nombre, user.email, user.fecha_registro))
        conn.commit()
        conn.close()

    def update_user(self, user):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Usuarios SET Nombre = ?, Email = ?, FechaRegistro = ? WHERE UsuarioID = ?", 
                       (user.nombre, user.email, user.fecha_registro, user.usuario_id))
        conn.commit()
        conn.close()

    def delete_user(self, user_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE UsuarioID = ?", (user_id,))
        conn.commit()
        conn.close()

    def insert_ingredient(self, ingredient):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ingredientes (Nombre, Descripción) VALUES (?, ?)", 
                       (ingredient.nombre, ingredient.descripcion))
        conn.commit()
        conn.close()

    def update_ingredient(self, ingredient):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Ingredientes SET Nombre = ?, Descripción = ? WHERE IngredienteID = ?", 
                       (ingredient.nombre, ingredient.descripcion, ingredient.ingrediente_id))
        conn.commit()
        conn.close()

    def delete_ingredient(self, ingrediente_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ingredientes WHERE IngredienteID = ?", (ingrediente_id,))
        conn.commit()
        conn.close()

    def get_user_by_id(self, user_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE UsuarioID = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(row['Nombre'], row['Email'], row['FechaRegistro'],row['UsuarioID'])
        return None

    def get_ingredient_by_id(self, ingrediente_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ingredientes WHERE IngredienteID = ?", (ingrediente_id,))
        row = cursor.fetchone()
        if row:
            return Ingredient(row['Nombre'], row['Descripción'], row['IngredienteID'])
        return None

    def get_all_users(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios")
        rows = cursor.fetchall()
        return [User(row['Nombre'], row['Email'], row['FechaRegistro'], row['UsuarioID']) for row in rows]

    def get_all_ingredients(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ingredientes")
        rows = cursor.fetchall()
        return [Ingredient(row['Nombre'], row['Descripción'], row['IngredienteID']) for row in rows]
















###########################################################
# def get_db_connection():
#     conn = sqlite3.connect(DATABASE_PATH)
#     return conn

# def create_db_from_sql(sql_file_path):
#     with open(sql_file_path, 'r') as sql_file:
#         sql_script = sql_file.read()
    
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.executescript(sql_script)
#     conn.commit()
#     conn.close()

# def init_db():
#     # Verificar si la base de datos existe, si no, crearla
#     if not os.path.exists(DATABASE_PATH):
#         print("No existe base de datos, se crea una vacía")
#         os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)  # Crea el directorio si no existe
#         create_db_from_sql(SQL_SCRIPT_PATH)
#     else:
#         print("Ya existe base de datos")


# def insert_user(nombre, email, fecha_registro):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO Usuarios (Nombre, Email, FechaRegistro) VALUES (?, ?, ?)', 
#                    (nombre, email, fecha_registro))
#     conn.commit()
#     conn.close()


# def insert_ingredient(nombre, descripcion):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO Ingredientes (Nombre, Descripción) VALUES (?, ?)', 
#                    (nombre, descripcion))
#     conn.commit()
#     conn.close()

# def get_all_users():
#     conn = get_db_connection()
#     users = conn.execute('SELECT * FROM Usuarios').fetchall()
#     conn.close()
#     return users

# def get_all_ingredients():
#     conn = get_db_connection()
#     ingredients = conn.execute('SELECT * FROM Ingredientes').fetchall()
#     conn.close()
#     return ingredients


# def update_user(user_id, nombre, email, fecha_registro):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # Actualizamos el nombre de la columna ID a UsuarioID para coincidir con tu esquema de DB
#     cursor.execute('UPDATE Usuarios SET Nombre = ?, Email = ?, FechaRegistro = ? WHERE UsuarioID = ?', 
#                    (nombre, email, fecha_registro, user_id))
#     conn.commit()
#     conn.close()

# def delete_user(user_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # Usamos UsuarioID como clave primaria
#     cursor.execute('DELETE FROM Usuarios WHERE UsuarioID = ?', (user_id,))
#     conn.commit()
#     conn.close()

# def update_ingredient(ingrediente_id, nombre, descripcion):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # Ajustamos el nombre de la columna ID a IngredienteID y corregimos 'Descripción' si necesario
#     cursor.execute('UPDATE Ingredientes SET Nombre = ?, Descripción = ? WHERE IngredienteID = ?', 
#                    (nombre, descripcion, ingrediente_id))
#     conn.commit()
#     conn.close()

# def delete_ingredient(ingrediente_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # Usamos IngredienteID como clave primaria
#     cursor.execute('DELETE FROM Ingredientes WHERE IngredienteID = ?', (ingrediente_id,))
#     conn.commit()
#     conn.close()


# def get_user_by_id(user_id):
#     conn = get_db_connection()
#     conn.row_factory = sqlite3.Row  # Configura el factory para devolver filas como diccionarios
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM Usuarios WHERE UsuarioID = ?', (user_id,))
#     user = cursor.fetchone()
#     conn.close()
#     if user:
#         return dict(user)  # Convierte la fila en un diccionario
#     else:
#         return None


# def get_ingrediente_by_id(ingrediente_id):
#     conn = get_db_connection()
#     conn.row_factory = sqlite3.Row  # Configura el factory para devolver filas como diccionarios
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM Ingredientes WHERE IngredienteID = ?', (ingrediente_id,))
#     ingrediente = cursor.fetchone()
#     conn.close()
#     if ingrediente:
#         return dict(ingrediente)  # Convierte la fila en un diccionario
#     else:
#         return None


