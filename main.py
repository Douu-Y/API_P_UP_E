
from fastapi import FastAPI, HTTPException
from database import crear_tabla_productos, crear_tabla_usuarios, crear_tabla_empleados, get_connection
from models import Productos, Usuarios, Empleados, Categorias
from psycopg import errors

app = FastAPI()

crear_tabla_productos()
crear_tabla_usuarios()
crear_tabla_empleados()


# -------------------------------------------------------------------
# Api_Productos

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de Productos"}


@app.get("/Productos")
def get_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()
    conn.close()
    
    return{"productos": productos}

@app.get("/Productos/{id}")
def buscar_producto(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, codigo, nombre, precio, stack FROM productos WHERE id = %s", (id,))
    producto = cur.fetchone()
    cur.close()
    conn.close()

    if producto:
        return {"producto": producto}
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.post("/Productos")
def create_producto(producto: Productos):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO " \
                    "productos(codigo, nombre, precio, stack) VALUES (%s, %s, %s, %s) " \
                    "RETURNING id", 
                    (producto.codigo, producto.nombre, producto.precio, producto.stack))
    new_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()

    return {"mensaje": "Producto Creado", "id": new_id}

@app.get("/productos/stock-bajo/{minimo}")
def productos_stock_bajo(minimo: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nombre, precio, stock, categoria_id FROM productos WHERE stock < %s ORDER BY id",
        (minimo,)
    )
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return {"productos": productos}

@app.put("/Productos/{id}")
def update_producto(id: int, producto: Productos):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM categorias WHERE id = %s", (producto.categoria_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="La categoría no existe")

    cur.execute(
        "UPDATE productos SET nombre = %s, precio = %s, stock = %s, categoria_id = %s WHERE id = %s",
        (producto.nombre, producto.precio, producto.stock, producto.categoria_id, id)
    )
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto actualizado"}

@app.delete("/Productos/{id}")
def delete_producto(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s", (id,))
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    
    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}

# endpoints de categorias

@app.post("/categorias")
def crear_categoria(categoria: Categorias):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorias WHERE nombre = %s", (categoria.nombre,))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    cur.execute(
        "INSERT INTO categorias (nombre) VALUES (%s) RETURNING id",
        (categoria.nombre,)
    )
    nuevo_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return {"Mensaje": "Categoría creada", "id": nuevo_id}


@app.get("/categorias")
def obtener_categorias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM categorias ORDER BY id")
    categorias = cur.fetchall()
    cur.close()
    conn.close()
    return {"categorias": categorias}


@app.get("/categorias/{categoria_id}")
def obtener_categoria(categoria_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM categorias WHERE id = %s", (categoria_id,))
    categoria = cur.fetchone()
    cur.close()
    conn.close()

    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@app.get("/categorias/{categoria_id}/productos")
def obtener_productos_por_categoria(categoria_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM categorias WHERE id = %s", (categoria_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    cur.execute(
        "SELECT id, nombre, precio, stock FROM productos WHERE categoria_id = %s ORDER BY id",
        (categoria_id,)
    )
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return {"productos": productos}


@app.delete("/categorias/{id}")
def eliminar_categoria(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM categorias WHERE id = %s", (id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    try:
        cur.execute("DELETE FROM categorias WHERE id = %s", (id,))
        conn.commit()
    except errors.RestrictViolation:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la categoría porque tiene productos asociados"
        )

    cur.close()
    conn.close()
    return {"mensaje": "Categoría eliminada"}


# -------------------------------------------------------------------
# Api_User_Password

@app.post("/Usuario/login")
def login_usuario(Usuario: Usuarios):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, Usuario FROM Usuarios WHERE Usuario = %s AND contraseña = %s",
        (Usuario.Usuario, Usuario.contraseña)
    )
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    if usuario:
        return {"mensaje": "el usuario existe"}
    else:
        raise HTTPException(status_code=404, detail="el usuario no existe")

# -------------------------------------------------------------------
# Api_Empleados

@app.get("/Empleados")
def get_empleados():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM empleados")
    empleados = cur.fetchall()
    cur.close()
    conn.close()
    
    return{"empleados": empleados}

@app.get("/Empleados/{id}")
def buscar_empleado(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, documento, nombre, cargo, salario FROM empleados WHERE id = %s", (id,))
    empleado = cur.fetchone()
    cur.close()
    conn.close()

    if empleado:
        return {"empleado": empleado}
    else:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")


@app.post("/Empleados")
def create_empleado(empleado: Empleados):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO " \
                    "empleados(documento, nombre, cargo, salario) VALUES (%s, %s, %s, %s) " \
                    "RETURNING id", 
                    (empleado.documento, empleado.nombre, empleado.cargo, empleado.salario))
    new_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()

    return {"mensaje": "Empleado Creado", "id": new_id}


@app.put("/Empleados/{id}")
def update_empleado(id: int, empleado: Empleados):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE empleados SET documento = %s, nombre = %s, cargo = %s, salario = %s WHERE id = %s",
                (empleado.documento, empleado.nombre, empleado.cargo, empleado.salario, id))
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return {"mensaje": "Empleado actualizado"}

@app.delete("/Empleados/{id}")
def delete_empleado(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM empleados WHERE id = %s", (id,))
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    
    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return {"mensaje": "Empleado eliminado"}