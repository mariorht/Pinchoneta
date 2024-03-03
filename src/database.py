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
        
class Bocadillo:
    def __init__(self, nombre, ingredientes=None, bocadillo_id=None):
        self.bocadillo_id = bocadillo_id
        self.nombre = nombre
        # Inicializa ingredientes como una lista vacía si no se proporciona ninguno
        self.ingredientes = ingredientes if ingredientes is not None else []




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


    def insert_bocadillo(self, bocadillo, ingredientes_ids):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Bocadillos (Nombre) VALUES (?)", (bocadillo.nombre,))
        bocadillo_id = cursor.lastrowid
        
        for ingrediente_id in ingredientes_ids:
            cursor.execute("INSERT INTO BocadilloIngredientes (BocadilloID, IngredienteID) VALUES (?, ?)", (bocadillo_id, ingrediente_id))
        
        conn.commit()
        conn.close()

    def get_all_bocadillos(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bocadillos")
        bocadillos_raw = cursor.fetchall()
        
        bocadillos = []
        for bocadillo_raw in bocadillos_raw:
            # Recuperar ingredientes para este bocadillo
            cursor.execute("""
                SELECT i.IngredienteID, i.Nombre, i.Descripción 
                FROM Ingredientes i 
                JOIN BocadilloIngredientes bi ON i.IngredienteID = bi.IngredienteID 
                WHERE bi.BocadilloID = ?
            """, (bocadillo_raw['BocadilloID'],))
            ingredientes_raw = cursor.fetchall()
            
            # Crear instancias de Ingredient para cada ingrediente
            ingredientes = [Ingredient(ingrediente_id=ing['IngredienteID'], nombre=ing['Nombre'], descripcion=ing['Descripción']) for ing in ingredientes_raw]
            
            # Crear instancia de Bocadillo con la lista de ingredientes
            bocadillo = Bocadillo(
                bocadillo_id=bocadillo_raw['BocadilloID'],
                nombre=bocadillo_raw['Nombre'],
                ingredientes=ingredientes
            )
            
            bocadillos.append(bocadillo)
        
        conn.close()
        return bocadillos
