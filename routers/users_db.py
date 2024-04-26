
# Creamos una API que se conecta con una base de datos LOCAL (con MongoDB)
# y que hace peticiones crud

from fastapi import APIRouter, HTTPException, status
from db.models.user import User # Importamos el modelo User, el cual ahora que trabajamos con MongoDB y mejor organización, lo importamos del archivo user.py
from db.schemas.user import user_schema, users_schema
from db.client import conectar_mongodb
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


users_list = []


@router.get("/", response_model=list[User])
async def users():
    return users_schema(conectar_mongodb().local.users.find())

@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id)) # Utilizamos la funcion ObjectId para buscar un objeto tipo id generado por MongoDB

@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
 
    user_dict = dict(user) # En MongoDB se trabaja con json o diccionarios, por lo cual convertimos el user en un diccionario 
    del user_dict["id"] # Evitamos que se inserte el campo id como NULL eliminándolo

    id = conectar_mongodb().local.users.insert_one(user_dict).inserted_id # Para acceder a la base de datos e insertar un nuevo user con solo username e email, y agregamos el id

    # Buscamos el usuario en la base de datos a través del id y lo recuperamos en new_user transformándolo de un json a un objeto tipo User con user_schema
    new_user = user_schema(conectar_mongodb().local.users.find_one({"_id": ObjectId(id)})) 

    return User(**new_user) # Retornamos objeto tipo User

@router.put("/", response_model=User, status_code=status.HTTP_202_ACCEPTED)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        conectar_mongodb().local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)

    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha actualizado el usuario")

    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, description="Usuario eliminado")
async def user(id: str):
    found = conectar_mongodb().local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha eliminado el usuario")


def search_user(field: str, key):

    try:
        user = user_schema(conectar_mongodb().local.users.find_one({field: key}))
        return User(**user)
    except:
        return {"Error":"No se ha encontrado el usuario"}


