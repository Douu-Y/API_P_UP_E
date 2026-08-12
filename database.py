import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE")

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

# -------------------------------------------------------------------
# Api_Productos

def crear_tabla_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categorias(
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL UNIQUE
        )
        """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    categoria_id INTEGER NOT NULL,
    CONSTRAINT fk_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categorias(id)
        ON DELETE RESTRICT
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# -------------------------------------------------------------------
# Api_User_Password

def crear_tabla_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios(
            id SERIAL PRIMARY KEY,
            Usuario VARCHAR(100) NOT NULL,
            contraseña varchar(100) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# -------------------------------------------------------------------
# Api_Empleados

def crear_tabla_empleados():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Empleados(
            id SERIAL PRIMARY KEY,
            documento INTEGER NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            cargo VARCHAR(100) NOT NULL,
            salario REAL NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()