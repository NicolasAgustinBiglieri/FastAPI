from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# OAuth2PasswordBearer es para gestionar la autenticación
# OAuth2PasswordRequestForm es la forma en la que se envía a nuestro backend el usuario y contraseña
# y en la que nuestro backend lo recibe

router = APIRouter()

# Creamos una instancia de nuestro sistema de autenticación OAUTH2
# y le pasamos la url donde se va a gestionar la autenticación
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Creamos una entidad usuario que usaremos para ir a través de la red, por lo cual sin contraseña
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# Creamos entidad usuario (la que estaría en un futuro del lado de la base de datos no relacional)
# Por lo cual al User le agregamos una contraseña (en este caso sin encriptación para aprender, luego la tendrá)
class UserDB(User):
    password: str

# Creamos usuarios que estarían en una DB, que usaremos para esta API de aprendizaje
users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "123456"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "654321"
    }
}

# Creamos una función para buscar el usuario en la base de datos
# Nos devuelve una instancia UserDB
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
# Utilizamos este User sin contraseña para devolverlo al validar el token
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
# Creamos una operación de autenticación para enviar usuario y contraseña
# A la función login le ponemos el parámetro form de tipo OAuth2PasswordRequestForm
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Comprobamos si tenemos el usuario ingresado
    user_db = users_db.get(form.username) # Recuperamos en una variable el usuario que se encuentra en la base de datos
    if not user_db: # Si no se encuentra el usuario, la variable estará vacía, entonces entra en este if not
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    # Buscamos al usuario como tal, recuperándolo en una instancia de tipo UserDB, para esto usamos search_user_db
    user = search_user_db(form.username) # Recuperamos en una variable de tipo UserDB el usuario a través del username
    if not form.password == user.password: # Controlamos el error de contraseña incorrecta
        raise HTTPException(status_code=400, detail="La contraseña es incorrecta")

    # Si la autenticación es correcta, hay que devolver un access token, en ese caso sin encriptación como práctica básica
    return {"access_token": user.username, "token_type": "bearer"} 


# Ya hicimos autenticación, ahora implementamos una operación que nos dé datos de usuario
# con dependencia a si estamos autenticados


# Creamos el criterio de dependencia que validará el token
async def current_user(token: str = Depends(oauth2)): # Va a depender del token que OAuth2PasswordBearer obtuvo del login
    user = search_user(token) # En este caso el token es igual al username, así que es sencillo.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled: # Si el usuario tiene disabled = True entra en este if y no tiene permisos
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")

    return user

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

