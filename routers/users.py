
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"],
                   responses={404: {"message": "No encontrado"}})

# Inicia el server con: uvicorn users:app --reload

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Brais", surname="Moure", url="http://moure.dev/", age=35),
              User(id=2, name="Moure", surname="Dev", url="http://mouredev.com/", age=35),
              User(id=3, name="Brais", surname="Pompin", url="http://pepe.pompin/", age=33)]

@router.get("/users_json")
async def users_json():
    return [{"name": "Pepe", "surname": "Pepon", "url": "https://mouredev.com/python" },
            {"name": "Pepe", "surname": "Peponcio", "url": "https://mouredev.com/python" },
            {"name": "Pepe", "surname": "Pepin", "url": "https://mouredev.com/python" }]

@router.get("/users")
async def users():
    return users_list

# Path (Usamos Path para los parametros que van fijos) (Ej: /cars para 
# luego buscar la patente de los vehiculos de los clientes)
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Query (Usamos Query para parametros dinamicos o parametros que pueden 
# no ser necesarios para hacer la peticion) (Ej: un id de un cliente)
@router.get("/user")
async def user(id: int):
    return search_user(id)

# Post: Operación Post para agregar usuarios
# A través de Thunder Client escribimos un json con todos los datos del nuevo usuario
# con un formato User

# @app.post("/user") # En este caso controlamos los errores y siempre devuelve 200 OK
# async def user(user: User):
#     if type(search_user(user.id)) == User:
#         return {"error": "El usuario ya existe"}
#     else:
#         users_list.append(user)
#         return user

# Agremamos especificación de Status (HTTP Status Code)
@router.post("/user", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user
    
# Put: Operación Put para actualizar el objeto completo
# Modo de uso similar al Post
@router.put("/user", status_code=202)
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="No se ha actualizado el usuario")
        # return {"error": "No se ha actualizado el usuario"}
    else:
        return user

# Delete: Operación Delete para eliminar un objeto completo
# Modo de uso similar al get, indicamos el path con el id que queremos eliminar, sin usar el body
@router.delete("/user/{id}", status_code=202, description="Usuario eliminado")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="No se ha eliminado el usuario")
        # return {"error": "No se ha eliminado el usuario"}
    else:
        return {"Finalizado": "Usuario eliminado"}

def search_user(id: int):
    users = filter (lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error":"No se ha encontrado el usuario"}
    
"""
POST: to create data.
GET: to read data.
PUT: to update data.
DELETE: to delete data.
"""


