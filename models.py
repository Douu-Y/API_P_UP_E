from pydantic import BaseModel

# -------------------------------------------------------------------
# Api_Productos

class Productos(BaseModel):
    nombre: str
    precio: float
    stock: int = 0
    categoria_id: int

class Categorias(BaseModel):
    nombre: str

# -------------------------------------------------------------------
# Api_User_Password

class Usuarios(BaseModel):
    Usuario: str
    contraseña: str

# -------------------------------------------------------------------
# Api_Empleados

class Empleados(BaseModel):
    documento: int
    nombre: str
    cargo: str
    salario: float