import sqlite3
import os

DATABASE_PATH = 'src/db/pinchonetaDB.db'
SQL_SCRIPT_PATH = 'src/db/empty_bbdd.sql'  # Asegúrate de poner la ruta correcta a tu archivo SQL

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def create_db_from_sql(sql_file_path):
    with open(sql_file_path, 'r') as sql_file:
        sql_script = sql_file.read()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

def init_db():
    # Verificar si la base de datos existe, si no, crearla
    if not os.path.exists(DATABASE_PATH):
        print("No existe base de datos, se crea una vacía")
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)  # Crea el directorio si no existe
        create_db_from_sql(SQL_SCRIPT_PATH)
    else:
        print("Ya existe base de datos")


def insert_user(nombre, email, fecha_registro):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Usuarios (Nombre, Email, FechaRegistro) VALUES (?, ?, ?)', 
                   (nombre, email, fecha_registro))
    conn.commit()
    conn.close()


def insert_ingredient(nombre, descripcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Ingredientes (Nombre, Descripción) VALUES (?, ?)', 
                   (nombre, descripcion))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM Usuarios').fetchall()
    conn.close()
    return users

def get_all_ingredients():
    conn = get_db_connection()
    ingredients = conn.execute('SELECT * FROM Ingredientes').fetchall()
    conn.close()
    return ingredients
